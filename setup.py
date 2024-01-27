from setuptools import setup, find_packages

setup(
    name='BookScanner',  
    version='0.1',  
    author='Nikodem Olsavsky',
    author_email='nikodem.olsavsky@gmail.com',
    description='Get list of books and their ratings from a bookshelf picture', 
    long_description=open('README.md').read(), 
    long_description_content_type='text/markdown', 
    #url='http://yourappwebsite.com',  
    packages=find_packages(), 
    install_requires=[
        # List your project's dependencies here
        # e.g., 'flask', 'detectron2', 'requests', etc.
    ],
    classifiers=[
        # Classifiers help users understand what your project is about
        # Full list: https://pypi.org/classifiers/
        'Development Status :: 4 - Beta',  # Change as appropriate
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Environment :: Web Environment',
        'Framework :: Flask',  # If you're using Flask, for example
    ],
    python_requires='>=3.6',  # Minimum version requirement of the package
    entry_points={
        'console_scripts': [
            'app=app.main:main',  # Replace 'yourapp.main:main' with your app's module path and function
        ],
    },
)
