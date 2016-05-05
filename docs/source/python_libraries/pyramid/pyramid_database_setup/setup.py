from setuptools import setup

requires = [
        'pyramid',
]

setup(
        name="database_app",
        install_requires=requires,
        entry_points="""\
        [paste.app_factory]
        main = database_app.app_config:main
        """,
)
