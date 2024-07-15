from setuptools import setup, find_packages

setup(
    name='gdUpload',
    version='0.0.7',
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
            'gdUpload=gdUpload.gdhandler:main',
        ],
    },
    author='Hammed A. Akande',
    author_email='akandehammedadedamola@gmail.com',
    description='A package to handle Google Drive uploads and downloads.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/drhammed/gdUpload',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
