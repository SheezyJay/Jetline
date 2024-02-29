from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

install_requires = [
    'click==8.1.7',
    'colorama==0.4.6',
    'toml==0.10.2',
    'pandas==2.2.0',
]

setup(
  name='Kiper',
  version='0.0.13',
  description='Pipeline Builder',
  #long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Johannes Kanthak',
  author_email='johannes.kanthak@kdc-solutions.de',
  license='MIT', 
  classifiers=classifiers,
  keywords='Pipeline', 
  packages=find_packages(),
  include_package_data=True,
  install_requires=install_requires,
  entry_points={
        'console_scripts': [
            'kiper-setup = kiper.commands.installer:setup_project'  # Befehl, der aufgerufen wird
        ],
    },
)