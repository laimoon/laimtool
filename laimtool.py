"""Doc..."""
import click

from laimenv import LaimLaim
from laimenv import STATUSES
from laimenv import (
    LaimEnvAlreadyExists,
    LaimEnvDoesNotExist,
    LaimEnvNotStopped)


laim = LaimLaim()


@click.group()
def cli():
    """Doc."""
    pass


@cli.command()
def envs():
    """Doc."""
    envs = '\n'.join(['- %s' % env for env in laim.envs()])
    click.echo('Running environments:\n' + '=' * 21 + '\n' + envs + '\n')


@cli.command()
@click.option('--name', prompt='Name',
              help='Give a name to your environment')
def start(name):
    """Doc."""
    try:
        status_code, container = laim.startenv(
            name=name,
        )
        click.echo("=" * 25 + "\n" + "Status: " + STATUSES.get(status_code))

        # if status_code == STOPPED:
        #     container.start()

    except LaimEnvAlreadyExists:
        if click.confirm("Environment already exists. Delete and continue?"):
            laim.delete(name)


@cli.command()
@click.option('--name', prompt='Name',
              help='Name of environment to delete')
def delete(name):
    """Doc."""
    try:
        laim.delete(name)
        click.echo('Environment "{}"" deleted.'.format(name))
    except LaimEnvDoesNotExist:
        click.echo('Environment "{}" does not exist.'.format(name))
    except LaimEnvNotStopped:
        if click.confirm("Environment not stopped. Stop and try again?"):
            laim.stop(name, wait=True)
            laim.delete(name)


@cli.command()
@click.option('--name', prompt='Name',
              help='Name of environment to activate')
def activate(name):
    """Doc."""
    try:
        click.echo('Activating "{}"...'.format(name))
        laim.bash(name)
        click.echo('Deactivating "{}"...'.format(name))
    except LaimEnvDoesNotExist:
        click.echo('Environment does not exist.')
