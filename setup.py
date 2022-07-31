from setuptools import find_packages
from setuptools import setup

with open('requirements.txt') as f:
    content = f.readlines()
requirements = [x.strip() for x in content if 'git+' not in x]

setup(
    name='game_assets',
    version="1.0",
    description="Helper functions to create game assets. simplify images etc",
    packages=find_packages(),
    install_requires=requirements,
    test_suite='tests',
    # include_package_data: to install data from MANIFEST.in
    include_package_data=True,
    #scripts=['scripts/game-assets-run'],
    zip_safe=False)
