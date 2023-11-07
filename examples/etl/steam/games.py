import requests
import logging
import cceyes
import pandas as pd
import cceyes.config as config
import cceyes.productions
import re
import time
from urllib.parse import urlparse, urlunparse
from cceyes.models import Production, ProductionDataset, ProductionMeta, ProductionReviews
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeRemainingColumn, TimeElapsedColumn
from rich.logging import RichHandler


FORMAT = "%(message)s"
logging.basicConfig(
    level="DEBUG", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)


def find_popular_games():
    url = "https://steamspy.com/api.php"
    response = requests.get(url, params={"request": "all", "page": 1})
    data = response.json()
    games = []

    steam_spy_all = pd.DataFrame.from_dict(data, orient='index')
    app_list = steam_spy_all[['appid', 'name', 'median_forever']].sort_values('appid').reset_index(drop=True)

    for index, row in app_list.iterrows():
        games.append(row)

    return games


def parse_steam_request(appid, name):
    """Unique parser to handle data from Steam Store API.

    Returns : json formatted data (dict-like)
    """
    url = "https://store.steampowered.com/api/appdetails/"
    parameters = {"appids": appid}

    data = requests.get(url, params=parameters)
    json_data = data.json()

    data = {'name': name, 'steam_appid': appid}

    if json_data is not None:
        json_app_data = json_data[str(appid)]

        if json_app_data['success']:
            data = json_app_data['data']

    return data


def create_production(row):
    game = parse_steam_request(row['appid'], row['name'])

    if game.get('detailed_description'):
        description = re.sub('<[^<]+?>', '', game['detailed_description'])

        if game.get('metacritic'):
            rating = round(float(game['metacritic']['score'] / 10), 2)
        else:
            rating = 5

        popularity = 0

        if row['median_forever'] > 8000:
            popularity = 10
        elif row['median_forever'] > 5000:
            popularity = 9
        elif row['median_forever'] > 3500:
            popularity = 8
        elif row['median_forever'] > 2000:
            popularity = 7
        elif row['median_forever'] > 1000:
            popularity = 6
        elif row['median_forever'] > 500:
            popularity = 5
        elif row['median_forever'] > 300:
            popularity = 4
        elif row['median_forever'] > 150:
            popularity = 3
        elif row['median_forever'] > 50:
            popularity = 2
        elif row['median_forever'] > 0:
            popularity = 1

        count = 0

        if game.get('recommendations'):
            count = game['recommendations']['total']

        publication_year = None

        if game.get('release_date'):
            if not game['release_date']['coming_soon']:
                publication_year = int(game['release_date']['date'].split(' ')[-1])

        parsed_image_url = urlparse(game['header_image'])
        clean_image_url = urlunparse(parsed_image_url._replace(query=""))

        production = Production(
            title=game['name'],
            content=description[:1000],
            dataset=ProductionDataset(
                type='Game',
                provider='Steam',
            ),
            meta=ProductionMeta(
                id=str(row['appid']),
                title=row['name'],
                image=clean_image_url,
                publication_year=publication_year,
                reviews=ProductionReviews(
                    rating=rating,
                    count=count,
                    popularity=popularity,
                )
            ),
        )

        return production

    return None


def main():
    log = logging.getLogger("rich")
    log.info(cceyes.providers.datasets().text)

    with Progress(
        SpinnerColumn(),
        TimeElapsedColumn(),
        BarColumn(),
        TimeRemainingColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        global_progress = progress.add_task("[red]Fetching Games…")
        games = find_popular_games()
        progress.update(global_progress, total=len(games))
        productions = []
        logging.debug(games)

        for game in games:
            log.debug(game['name'])

            progress.update(global_progress, advance=0.1, description=game['name'])

            # Check if already exists
            # production = cceyes.productions.find(
                # ProductionDataset(type='Game', provider='Steam'),
                # ProductionMeta(id=str(game['appid']), title=game['name'])
            # )

            progress.update(global_progress, advance=0.1)

            # if production:
                # progress.update(global_progress, advance=0.8)
                # continue

            # Create production
            production = create_production(game)
            print(production)

            if production is not None:
                # Add the production to the list
                productions.append(production)

                time.sleep(1)

            progress.update(global_progress, advance=0.6)

            # If we have 30 productions, send them to the API
            if len(productions) == 30:
                response = cceyes.providers.upsert(productions)
                log.debug(response.text)

                progress.update(global_progress, advance=0.3*10)
                productions = []

                time.sleep(5)

        response = cceyes.providers.upsert(productions)
        log.debug(response.text)

        progress.update(global_progress, advance=len(games))


if __name__ == "__main__":
    main()
