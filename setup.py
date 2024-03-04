from setuptools import setup, find_packages

classifiers = [
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
]

install_requires = [
    'click==8.1.7',
    'colorama==0.4.6',
    'toml==0.10.2',
    'pandas==2.2.0',
    'openpyxl==3.1.2',
    'coloredlogs==15.0.1',
    'fastapi==0.110.0',
    

]

setup(
    name='jetline',
    version='0.0.49',
    description='Automated Pipeline Builder',
    url='https://github.com/your_username/jetline',
    author='Johannes Kanthak',
    author_email='johannes.kanthak@kdc-solutions.de',
    license='MIT',
    classifiers=classifiers,
    keywords='pipeline automation',
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'jetline = jetline.commands.info:main',
            'jetline-setup = jetline.commands.installer:main',
            'jetline-create-pipe = jetline.commands.create_pipe:main',
            'jetline-analyze = jetline.commands.analyze_project:main',
            'jetline-run = jetline.commands.run_pipeline:main [args]',
            'jetline-to-exe = jetline.commands.to_exe:main'
        ],
    },
)
