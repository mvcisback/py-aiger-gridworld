from setuptools import find_packages, setup

DESC = 'Grid-world to aiger circuit library.'

setup(
    name='py-aiger-gridworld',
    version='0.0.0',
    description=DESC,
    url='http://github.com/mvcisback/py-aiger-gridworld',
    author='Marcell Vazquez-Chanlatte',
    author_email='marcell.vc@eecs.berkeley.edu',
    license='MIT',
    install_requires=[
        'py-aiger',
        'py-aiger-bv',
        'funcy'
    ],
    packages=find_packages(),
)
