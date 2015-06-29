from setuptools import setup

requires = [
        'pyramid',
        'pyramid_mako',
]

setup(name="app_example",
        install_requires=requires,
        entry_points="""\
        [paste.app_factory]
        main = app_example.setup_app:main
        """,
)
