from setuptools import setup, find_packages

setup(
    name="synchro",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'synchro=synchro_tool:main',  # 'synchro' is the command, 'synchro_tool:main' specifies the function
        ],
    },
    install_requires=[
        'toml',  # List all the dependencies here
        'termcolor', # and any others you use
    ],
)
