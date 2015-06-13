from setuptools import setup

setup(
    name = 'ular',
    description = 'Snake',
    author = 'Mohd Tarmizi Mohd Affandi',
    author_email = 'tarmiziaffandi@yahoo.com',
    install_requires = ['pyglet>=1.2'],
    packages = ['ular'],
    package_data = {'ular': [
        'sprites.png',
    ]},
)
