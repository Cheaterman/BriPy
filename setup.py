from setuptools import find_packages, setup

setup(
    name='BriPy',
    version='0.1',
    packages=find_packages(),
    entry_points={'console_scripts': [
        'bripy = bripy:main',
        'bripy-ac = bripy:ac',
        'bripy-battery = bripy:battery',
    ]},
    author='Cheaterman',
    author_email='the.cheaterman@gmail.com',
    description='Control the backlight through sysfs',
    license='MIT',
)
