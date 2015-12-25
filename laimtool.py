import click
from laimenv import LaimLaim
laim = LaimLaim()


@click.group()
def cli():
    click.echo("Run a command!")
    pass


@cli.command()
def envs():
    click.echo(['- %s\n' % env for env in laim.envs()])


@cli.command()
@click.option('--env_name', prompt='Env name',
              help='Give a name to your environment')
@click.option('--source_type', prompt='Source type',
              help='Choose between: ' + ' '.join(
                  st for st in laim.SOURCE_TYPE))
@click.option('--source_alias', prompt='Source alias',
              help="If it's an image, type in the alias name of the image")
def startenv(env_name, source_type, source_alias):
    c = laim.startenv(
        name=env_name,
        source_type='image',
        source_alias=source_alias,
        profiles=['default'],
        conf={},
        ephemeral=False
    )
    click.echo(c)
