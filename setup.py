from setuptools import setup, find_packages

setup(
    name = "Pagetags",
    version = "0.1",
    packages = find_packages(exclude=["tests"]),
    install_requires = [
        "Flask==0.11.1",
        "Flask-Script==2.0.5",
        "Flask-SQLAlchemy==2.1",
        "Flask-WTF==0.12",
        "Flask-Login==0.3.2",
        "Flask-JWT==0.3.2",
        "Flask-RESTful==0.3.5",
        "alembic==0.8.7",
        "psycopg2==2.6.2",
        "Flask-Admin==1.4.2"
    ],
    include_package_data=True,
    zip_safe=False,
    setup_requires=["nose==1.3.7"],
    tests_require=["nose==1.3.7"],
    test_suite = 'nose.collector',
    entry_points={
        'console_scripts': [
            'pagetags = pagetags.cli:main',
        ]
    }
)
