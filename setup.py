from setuptools import setup, find_packages

setup(
        name='your_package_name',
        version='0.1.0',
        packages=find_packages(),
        entry_points={
            'console_scripts': [
                'json2py=json2py.main:main',
            ],
        },
)
