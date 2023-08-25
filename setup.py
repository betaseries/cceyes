from setuptools import setup, find_packages

setup(
    name="cceyes",
    version="{{VERSION_PLACEHOLDER}}",
    long_description="file: README.md",
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires='>=3.6, <4',
    install_requires=[
        'requests',
        'typer',
        'PyYAML'
    ],
    entry_points={
        'console_scripts': [
            'cceyes=cceyes.main:app',
        ],
    },
)
