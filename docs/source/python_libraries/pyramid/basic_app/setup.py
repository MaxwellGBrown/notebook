from setuptools import setup

requires = [
        'pyramid',
]

setup(
        name="basic_app",
        install_requires=requires,
        entry_points="""\
        [paste.app_factory]
        main = basic_app.setup_app:main
        """,
)
