from setuptools import setup

setup(
    name='tumblr-upload',
    version='0.1',
    entry_points={
        'console_scripts': {'tumblr-upload = tumblr_upload.cli:cli'}
    }
)
