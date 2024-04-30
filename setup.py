from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='jetline',
    version='1.0.0',
    description='Automated Pipeline Builder',
    url='https://github.com/your_username/jetline',
    author='Johannes Kanthak',
    author_email='johannes.kanthak@kdc-solutions.de',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    packages=find_packages(),
    include_package_data=True,

    install_requires= requirements,
    entry_points={
        'console_scripts': [
            'jetline = jetline.commands.info:main',
            'jetline-setup = jetline.commands.installer:main',
            'jetline-create-pipe = jetline.commands.create_pipe:main',
            'jetline-viz = jetline.commands.create_viz:main',
            'jetline-run = jetline.commands.run_pipeline:main [args]',
            'jetline-to-exe = jetline.commands.to_exe:main'
        ],
    },
)
