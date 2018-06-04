import logging
import os
from glob import glob
from typing import Dict, List

import click
import pytumblr
import yaml
from PIL import Image
from termcolor import colored

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


def ensure_dir(dirname: str) -> None:
    if not os.path.exists(dirname):
        os.makedirs(dirname)


def archive(infile: str) -> str:
    basename = os.path.basename(infile)
    archivefile = os.path.join(ARCHIVE_DIR, basename)
    ensure_dir(ARCHIVE_DIR)
    os.rename(infile, archivefile)
    return archivefile


def render_tags(tags: List[str]) -> str:
    return ', '.join(map(lambda x: f'#{x}', tags))


def parse_tags(tags: str) -> List[str]:
    return list(map(lambda x: x.strip(), tags.split(',')))


def upload(blogname:str , path: str, show: bool) -> None:
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
            archivefile = archive(path)
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
