from setuptools import setup, find_packages

setup(
    name='GDriveOps',
    version='0.1.9',
    packages=find_packages(),
    install_requires=[
        "google-api-python-client",
        "google-auth",
        "google-auth-httplib2",
        "google-auth-oauthlib",
        'PyMuPDF',
        'python-docx',
        'nltk',
        'streamlit',
        'openai',
        'voyageai',
        'langchain',
        'langchain-openai',
        'langchain-voyageai',
        'langchain-groq',
        'langchain-core',
        'scikit-learn',
        'rouge-score',  
    ],
    dependency_links=[
        'https://pypi.org/simple/'
    ],
    entry_points={
        'console_scripts': [
            'GDriveOps=GDriveOps.GDhandler:main',
            'GDriveOps-app=GDriveOps.app:main',
        ],
    },
    author='Hammed A. Akande',
    author_email='akandehammedadedamola@gmail.com',
    description='A package to handle Google Drive uploads and downloads.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/drhammed/GDriveOps',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)