import requests
import json
import sys
import typer
from . import providers, config

app = typer.Typer()


@app.callback()
def main():
    """
    CCEyes CLI
    """
    config.init()


@app.command()
def key():
    api_key = typer.prompt("Enter your API key", hide_input=True)
    config.set_config('api', 'key', api_key)

    print("API key saved!")


@app.command()
def set_config(
    parent: str = typer.Argument(..., help="Parent key"),
    key: str = typer.Argument(..., help="Key"),
    value: str = typer.Argument(..., help="Value"),
):
    """
    Set a config value
    """
    config.set_config(parent, key, value)

    print("Config value saved!")


@app.command()
def me():
    """
    Display providers associated with the key
    """
    response = providers.me()

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
