from setuptools import setup, find_packages

setup(
        name='httpfs',
        version='0.1',
        packages=find_packages(),
        entry_points={'console_scripts': 'httpfs = httpfs.__init__:cli'},
)
