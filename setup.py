from distutils.core import setup
from pathlib import Path

this_dir = Path(__file__).parent

with open(this_dir / 'requirements.txt') as file:
    requirements = '\n'.join(file.readlines())

with open(this_dir / 'README.md') as file:
    long_description = file.read()

setup(
    name='dvdp.ha_mqtt',
    version='0.2.0',
    packages=['dvdp.ha_mqtt'],
    download_url='https://github.com/davidvdp/ha_mqtt/archive/v0.1.0.tar.gz',
    url='https://github.com/davidvdp/ha_mqtt',
    author='David van der Pol',
    author_email='david@davidvanderpol.com',
    license='MIT',
    description='Home assistant mqtt devices interface',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=requirements,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    keywords=[
        'MQTT',
        'Home',
        'Assistant',
    ],
)