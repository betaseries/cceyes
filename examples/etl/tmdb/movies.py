import requests
import logging
import cceyes
import pandas as pd
import cceyes.config as config
import cceyes.productions
import time
from cceyes.models import Production, ProductionDataset, ProductionMeta
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeRemainingColumn, TimeElapsedColumn
from rich.logging import RichHandler


FORMAT = "%(message)s"
logging.basicConfig(
    level="DEBUG", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)


def find_popular_movies():
    url = "https://api.themoviedb.org/3/movie/popular"
    movies = []

    for page in range(51, 101):
        params = {'api_key': config.get_config('tmdb', 'key'), 'page': page}
        response = requests.get(url, params=params)

        if response.status_code != 200:
            logging.debug(f"Failed to get data for page {page}, status code: {response.status_code}")
            continue

        data = response.json()
        movies.extend(data['results'])

        # sleep
        time.sleep(1)

    return movies


def create_production(movie):
    production = Production(
        title=movie['title'],
        content=movie['overview'][:1000],
        dataset=ProductionDataset(
            type='Movie',
            provider='TMDB',
        ),
        meta=ProductionMeta(
            id=str(movie['id']),
            title=movie['title'],
            image=f"https://image.tmdb.org/t/p/original/{movie['poster_path']}",
        ),
    )

    return production


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
        global_progress = progress.add_task("[red]Fetching Movies…")
        movies = find_popular_movies()
        progress.update(global_progress, total=len(movies))
        productions = []
        logging.debug(movies)

        for movie in movies:
            log.debug(movie['title'])

            progress.update(global_progress, advance=0.1, description=movie['title'])

            # Check if already exists
            # production = cceyes.productions.find(
            #    ProductionDataset(type='Movie', provider='TMDB'),
            #    ProductionMeta(id=str(movie['id']), title=movie['title'])
            # )

            progress.update(global_progress, advance=0.1)

            # if production:
            #    progress.update(global_progress, advance=0.8)
            #    continue

            # Create production
            production = create_production(movie)
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

        progress.update(global_progress, advance=len(movies))


if __name__ == "__main__":
    main()
