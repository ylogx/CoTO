import click

import coto


@click.group()
def cli():
    pass


@cli.command()
def book_newer_slot():
    driver = coto.driver.driver()
    coto.procedure.new_slot(driver)


if __name__ == "__main__":
    cli()
