from distutils.core import setup

with open('requirements.txt') as file:
    requirements = '\n'.join(file.readlines())

setup(
    name='dvdp.ha_mqtt',
    version='0.1.0',
    packages=['dvdp.ha_mqtt'],
    url='',
    author='David van der Pol',
    description=open('README.md').read(),
    python_requires='>=3.7',
    install_requires=requirements,
)