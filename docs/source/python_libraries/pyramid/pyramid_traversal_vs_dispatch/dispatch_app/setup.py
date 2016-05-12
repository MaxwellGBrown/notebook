from setuptools import setup

requires = [
        'pyramid',
        'pyramid_mako',
]

setup(
        name="dispatch_app",
        install_requires=requires,
        entry_points="""\
        [paste.app_factory]
        main = dispatch_app.app_config:main
        """,
)
