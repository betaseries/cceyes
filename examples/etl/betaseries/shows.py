import requests
import logging
import utils
import cceyes
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeRemainingColumn, TimeElapsedColumn
from rich.logging import RichHandler

FORMAT = "%(message)s"
logging.basicConfig(
    level="DEBUG", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)


def find_popular_shows(number=100):
    start = 0
    all_tv_shows = []

    while start < number:
        url = f"https://api.betaseries.com/shows/list?limit=100&order=popularity&locale=en&start={start}"
        response = requests.get(url, headers=utils.headers)
        tv_shows = response.json()['shows']

        if not tv_shows:
            break

        if number < 100:
            tv_shows = tv_shows[:number]

        all_tv_shows.extend(tv_shows)
        start += 100

    return all_tv_shows


def create_meta(tv_show):
    # Fetch the TV series details
    return {
        'id': tv_show['id'],
        'title': tv_show['title'],
        'image': tv_show['images']['poster'],
    }


def create_content(tv_show):
    # Fetch the TV series details including the synopsis
    return f"{tv_show['title']}: {tv_show['description']}"


def main():
    log = logging.getLogger("rich")
    log.info(cceyes.providers.me().text)

    with Progress(
        SpinnerColumn(),
        TimeElapsedColumn(),
        BarColumn(),
        TimeRemainingColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        global_progress = progress.add_task("[red]Fetching TV Series…")
        tv_shows = find_popular_shows(100)
        progress.update(global_progress, total=len(tv_shows))
        productions = []

        for tv_show in tv_shows:
            log.debug(tv_show['title'])

            progress.update(global_progress, advance=0.1, description=tv_show['title'])

            meta = create_meta(tv_show)
            progress.update(global_progress, advance=0.2)

            content = create_content(tv_show)
            progress.update(global_progress, advance=0.2)

            # Add the production to the list
            productions.append({
                'title': meta["title"],
                'content': content,
                'reference': {
                    'type': 'TV Series',
                    'provider': 'BetaSeries',
                },
                'meta': {
                    'id': meta["id"],
                    'title': meta["title"],
                    'image': meta['image'],
                },
            })
            progress.update(global_progress, advance=0.2)

            # If we have 10 productions, send them to the API
            if len(productions) == 10:
                response = cceyes.providers.upsert(productions)
                log.debug(response.text)

                progress.update(global_progress, advance=0.3*10)
                productions = []


if __name__ == "__main__":
    main()