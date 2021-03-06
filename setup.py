from setuptools import setup, find_packages

setup(
    name="Pagetags",
    version="0.2.0",
    packages=find_packages(exclude=["tests"]),
    install_requires=[
        "Flask==0.11.1",
        "Flask-Script==2.0.5",
        "Flask-SQLAlchemy==2.1",
        "Flask-WTF==0.12",
        "Flask-Login==0.3.2",
        "Flask-JWT==0.3.2",
        "Flask-RESTful==0.3.5",
        "alembic==0.8.7",
        "psycopg2==2.6.2",
        "Flask-Admin==1.4.2",
        "uWSGI==2.0.14",
        "Sphinx==1.5.2",
        "sphinxcontrib-httpdomain==1.5.0",
        "PyJWT==1.4.2",
        "arrow==0.10.0",
        "flask-restful-swagger==0.19"
    ],
    include_package_data=True,
    zip_safe=False,
    setup_requires=["nose==1.3.7"],
    tests_require=[
        "nose==1.3.7",
        "mock==2.0.0"
    ],
    test_suite = 'nose.collector',
    entry_points={
        'console_scripts': [
            'pagetags=pagetags.cli.commands:main',
        ]
    }
)
