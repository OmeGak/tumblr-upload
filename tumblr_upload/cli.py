import logging
import os
from glob import glob
from typing import List

import click
import pytumblr
import yaml
from PIL import Image
from termcolor import colored

from .util import archive, parse_tags, render_tags

ARCHIVE_DIR = 'uploaded'
TAGS_FILE = 'tags.yml'
TUMBLR_KEYS_FILE = os.path.expanduser('~/.tumblr')

logger = logging.getLogger()
global_tags: List[str] = []

with open(TUMBLR_KEYS_FILE, 'r') as f:
    tokens = yaml.load(f)['tokens']
client = pytumblr.TumblrRestClient(**tokens)

if os.path.exists(TAGS_FILE):
    with open(TAGS_FILE, 'r') as f:
        global_tags = global_tags + yaml.load(f)['tags']


def upload(blogname: str, path: str, show: bool) -> None:
    if show:
        Image.open(path).show()
    caption = click.prompt("  Add caption", default='', show_default=False)
    tags_str = click.prompt("  Add extra tags (separated by comma)", default='', show_default=False)
    tags = global_tags
    if tags_str:
        tags = tags + parse_tags(tags_str)
    click.echo(f"  Caption: \"{caption}\"")
    click.echo(f"  Tags: {render_tags(tags)}")
    if click.confirm(f"  Upload?", default=True):
        response = client.create_photo(blogname, data=path, state='queue', caption=caption, tags=tags)
        logger.debug(response)
        if 'response' not in response:
            archivefile = archive(path, ARCHIVE_DIR)
            click.echo(colored(f"  Archived as {archivefile}", 'green'))
            click.echo()
        else:
            raise Exception("Pic couldn't get uploaded")


@click.command()
@click.argument('blogname', type=str)
@click.argument('path', type=click.Path(exists=True), default='.')
@click.option('--quiet', '-q', is_flag=True)
def cli(blogname: str, path: str, quiet: bool) -> None:
    filenames = sorted(glob('{}/*.jpg'.format(path)))
    for idx, filename in enumerate(filenames):
        click.echo(f"Processing {filename} ({idx+1}/{len(filenames)})...")
        upload(blogname, filename, show=not quiet)
