from setuptools import setup

setup(name='tumblrupload',
      version='0.1',
      entry_points='''
            [console_scripts]
            tumblr-upload=script:cli
      ''')
