import requests
import json
import sys
import typer
from . import providers, config as config_module

app = typer.Typer()


@app.callback()
def main():
    """
    CCEyes CLI
    """
    config_module.init()


@app.command()
def key():
    api_key = typer.prompt("Enter your API key", hide_input=True)
    config_module.set_config('api', 'key', api_key)

    print("API key saved!")


@app.command()
def config(
    parent: str = typer.Argument(..., help="Parent key"),
    key: str = typer.Argument(..., help="Key"),
    value: str = typer.Argument(..., help="Value"),
):
    """
    Set a config value
    """
    config_module.set_config(parent, key, value)

    print("Config value saved!")


@app.command()
def datasets():
    """
    Display datasets associated with the key
    """
    response = providers.datasets()

    print(response.text)


@app.command()
def stats():
    """
    Display datasets stats
    """
    response = providers.stats()

    print(response.text)


@app.command()
def upsert():
    """
    Upsert productions into the CCEyes database
    """
    response = providers.upsert(json.loads(sys.stdin.read()))

    print(response.text)


if __name__ == "__main__":
    app()
