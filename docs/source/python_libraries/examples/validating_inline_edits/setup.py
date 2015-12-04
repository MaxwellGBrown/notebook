from setuptools import setup

requires = [
        'pyramid',
        'pyramid_mako',
]

setup(
        name="inline_app",
        install_requires=requires,
        entry_points="""\
        [paste.app_factory]
        main = inline_app.setup_app:main
        """,
)
