from setuptools import setup

requires = [
        'pyramid',
        'pyramid_mako',
]

setup(
        name="full_auth_app",
        install_requires=requires,
        entry_points="""\
        [paste.app_factory]
        main = full_auth_app.app_config:main
        """,
)
