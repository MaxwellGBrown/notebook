from setuptools import setup

requires = [
        'pyramid',
]

setup(name="example_app",
        install_requires=requires,
        entry_points="""\
                [paste.app_factory]
                main = example_app:main
                """,
)
