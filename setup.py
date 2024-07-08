# setup.py

from setuptools import setup, find_packages

setup(
    name='my_google_drive_package',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'google-auth',
        'google-auth-oauthlib',
        'google-auth-httplib2',
        'google-api-python-client',
        'PyMuPDF',
        'python-docx',
    ],
    entry_points={
        'console_scripts': [
            'google_drive_handler=my_google_drive_package.google_drive_handler:main',
        ],
    },
)
