"""Setup script for the Data Pipeline DAGs project.
"""
import os
import setuptools

PROJECT_NAME = os.path.basename(os.path.abspath(os.curdir))

PROD_PACKAGES = [
]

DEV_PACKAGES = [
    'apache-airflow==1.10.11',
    'pylint',
    'pytest',
    'pytest-cov',
    'pytest-sugar',
]

PACKAGES = list(PROD_PACKAGES)
if (os.environ.get('APP_ENV') and 'dev' in os.environ.get('APP_ENV')):
    PACKAGES += DEV_PACKAGES

SETUP_KWARGS = {
    'name': PROJECT_NAME,
    'version': '0.0.0',
    'description': 'Data Pipeline DAGs',
    'author': 'Lou Markovski',
    'author_email': 'lou.markovski@gmail.com',
    'url': 'https://github.com/loum/data-pipeline-dags',
    'install_requires': PACKAGES,
    'packages': setuptools.find_namespace_packages(include=['data_pipelines_dags.*'],
                                                   exclude=['*.tests', '*.tests.*', 'tests.*', 'tests']),
    'include_package_data': True,
    'license': 'MIT',
    'classifiers': [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
}

setuptools.setup(**SETUP_KWARGS)
