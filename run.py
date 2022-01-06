import click

import coto


@click.group()
def cli():
    pass


@cli.command()
def book_newer_slot():
    driver = coto.driver.driver()
    info = coto.data.get_data()
    coto.procedure.new_slot(driver, info)


if __name__ == "__main__":
    cli()
