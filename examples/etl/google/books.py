import requests
import logging
import cceyes
import cceyes.config as config
from cceyes.models import Production, ProductionDataset, ProductionMeta
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeRemainingColumn, TimeElapsedColumn
from rich.logging import RichHandler

FORMAT = "%(message)s"
logging.basicConfig(
    level="DEBUG", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)


def find_popular_books(num_books=40, start_index=0):
    key = config.get_config('google', 'key')
    base_url = f"https://www.googleapis.com/books/v1/volumes?key={key}"
    params = {
        "q": "subject:fiction",  # You can modify the query to suit your needs
        "orderBy": "newest",
        "maxResults": 40,
        "langRestrict": "en",
        "startIndex": start_index,
    }

    books = []

    while start_index < num_books:
        params['startIndex'] = start_index
        response = requests.get(base_url, params=params)
        data = response.json()
        logging.debug(data)

        popular_books = data.get("items", [])

        for book in popular_books:
            volume_info = book.get("volumeInfo", {})

            books.append({
                "id": book["id"],
                "title": volume_info.get("title", "N/A"),
                "authors": ", ".join(volume_info.get("authors", ["N/A"])),
                "publish_date": volume_info.get("publishedDate", "N/A"),
                "description": volume_info.get("description", "N/A"),
                "cover": volume_info.get("imageLinks", {}).get("thumbnail", ""),
            })

        start_index += 40

    return books


def create_meta(book):
    # Fetch the book details
    return {
        'id': book['id'],
        'title': book['title'],
        'image': book['cover'],
    }


def create_content(book):
    # Fetch the TV series details including the synopsis
    content = f"{book['title']}: {book['description']}"

    # Limit to 1000 characters
    return content[:1000]


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
        global_progress = progress.add_task("[red]Fetching Books…")
        books = find_popular_books(1000, 0)
        progress.update(global_progress, total=len(books))
        productions = []
        logging.debug(books)

        for book in books:
            log.debug(book['title'])

            progress.update(global_progress, advance=0.1, description=book['title'])

            meta = create_meta(book)
            progress.update(global_progress, advance=0.2)

            content = create_content(book)
            progress.update(global_progress, advance=0.2)

            # Add the production to the list
            productions.append(Production(
                title=meta["title"],
                content=content,
                dataset=ProductionDataset(
                    type='Book',
                    provider='Google',
                ),
                meta=ProductionMeta(
                    id=meta["id"],
                    title=meta["title"],
                    image=meta['image'],
                ),
            ))

            progress.update(global_progress, advance=0.2)

            # If we have 30 productions, send them to the API
            if len(productions) == 30:
                response = cceyes.providers.upsert(productions)
                log.debug(response.text)

                progress.update(global_progress, advance=0.3*10)
                productions = []

        response = cceyes.providers.upsert(productions)
        log.debug(response.text)

        progress.update(global_progress, advance=len(books))


if __name__ == "__main__":
    main()
