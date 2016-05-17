from setuptools import setup

requires = [
        'pyramid',
        'pyramid_mako',  # newly added
]

setup(
        name="hybrid_app",
        install_requires=requires,
        entry_points="""\
        [paste.app_factory]
        main = hybrid_app.app_config:main
        """,
)
