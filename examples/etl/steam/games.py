import requests
import logging
import cceyes
import pandas as pd
import cceyes.config as config
import cceyes.productions
import re
from cceyes.models import Production, ProductionDataset, ProductionMeta
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeRemainingColumn, TimeElapsedColumn
from rich.logging import RichHandler


FORMAT = "%(message)s"
logging.basicConfig(
    level="DEBUG", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)


def find_popular_games():
    url = "https://steamspy.com/api.php"
    response = requests.get(url, params={"request": "all"})
    data = response.json()
    games = []

    steam_spy_all = pd.DataFrame.from_dict(data, orient='index')
    app_list = steam_spy_all[['appid', 'name']].sort_values('appid').reset_index(drop=True)

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
                image=game['header_image'],
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
            production = cceyes.productions.find(
                ProductionDataset(type='Game', provider='Steam'),
                ProductionMeta(id=str(game['appid']), title=game['name'])
            )

            progress.update(global_progress, advance=0.1)

            if production:
                progress.update(global_progress, advance=0.8)
                continue

            # Create production
            production = create_production(game)
            print(production)

            if production is not None:
                # Add the production to the list
                productions.append(production)

            progress.update(global_progress, advance=0.6)

            # If we have 30 productions, send them to the API
            if len(productions) == 30:
                response = cceyes.providers.upsert(productions)
                log.debug(response.text)

                progress.update(global_progress, advance=0.3*10)
                productions = []

        response = cceyes.providers.upsert(productions)
        log.debug(response.text)

        progress.update(global_progress, advance=len(games))


if __name__ == "__main__":
    main()
