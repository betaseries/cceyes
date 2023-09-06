from setuptools import setup, find_packages
import sys
sys.path.insert(0, ".")  # noqa
import versioneer
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="cceyes",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
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
