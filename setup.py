from setuptools import setup

setup(
    name='google-music-downloader',
    version='0.1',
    scripts=['gmusic-dl.py'],
    install_requires=[
        'eyed3>=0.8.0b1',
        'gmusicapi',
        'goldfinch',
        'pathlib'
    ]
)