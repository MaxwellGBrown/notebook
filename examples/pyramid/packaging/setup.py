from setuptools import setup

requires = [
        'pyramid',
]

setup(name="app_example",
        install_requires=requires,
        entry_points="""\
                [paste.app_factory]
                main = app_example.setup_app:main
                """,
)
