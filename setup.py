from setuptools import setup, find_packages
from setuptools.command.install import install


class InstallCommand(install):
    def run(self):
        install.run(self)
        import nltk
        nltk.download('wordnet')

setup(
        name='json2py',
        version='0.1.0',
        packages=find_packages(),
        entry_points={
            'console_scripts': [
                'json2py=json2py.main:main',
            ],
        },
        install_requires=['nltk'],
        setup_requires=['nltk'],
        cmdclass={
            'install': InstallCommand,
        }
)