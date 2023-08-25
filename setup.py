from setuptools import setup, find_packages

setup(
    name="cceyes",
    version="{{VERSION_PLACEHOLDER}}",
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
