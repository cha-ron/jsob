from setuptools import setup

setup(
    name='jsob',
    py_modules=['jsob'],
    install_requires=[
        'Click'
    ],
    entry_points='''
        [console_scripts]
        jsob=jsob:cli
    '''
)
