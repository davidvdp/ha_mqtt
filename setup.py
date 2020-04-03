from distutils.core import setup

with open('requirements.txt') as file:
    requirements = '\n'.join(file.readlines())

setup(
    name='dvdp.ha_mqtt',
    version='0.1.0',
    packages=['dvdp.ha_mqtt'],
    url='https://github.com/davidvdp/ha_mqtt',
    author='David van der Pol',
	license='MIT',
	description='Home assistant mqtt devices interface'
    long_description=open('README.md').read(),
    python_requires='>=3.7',
    install_requires=requirements,
	include_package_data=True,
	classifiers=[
		'Programming Language :: Python :: 3'
		'Programming Language :: Python :: 3.7'
	],
)