from setuptools import setup

setup(
    name='laimtool',
    version='0.1',
    py_modules=[
        'laimtool'
    ],
    
    install_requires=[
        'click',
    ],

    entry_points='''
        [console_scripts]
        laimtool=laimtool:cli
    '''
)