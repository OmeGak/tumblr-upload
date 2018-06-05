import os
from typing import List


def archive(infile: str, archive_dir: str) -> str:
    basename = os.path.basename(infile)
    archivefile = os.path.join(archive_dir, basename)
    ensure_dir(archive_dir)
    os.rename(infile, archivefile)
    return archivefile


def ensure_dir(dirname: str) -> None:
    if not os.path.exists(dirname):
        os.makedirs(dirname)


def render_tags(tags: List[str]) -> str:
    return ', '.join(map(lambda x: f'#{x}', tags))


def parse_tags(tags: str) -> List[str]:
    return list(map(lambda x: x.strip(), tags.split(',')))
