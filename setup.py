from setuptools import setup, find_packages

# read the contents of the README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="cceyes",
    version="0.2.1",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires='>=3.6, <4',
    install_requires=[
        'requests',
        'typer',
        'PyYAML',
        'pydantic',
    ],
    entry_points={
        'console_scripts': [
            'cceyes=cceyes.main:app',
        ],
    },
)
