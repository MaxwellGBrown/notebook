from setuptools import setup

requires = [
        'pyramid',
        'pyramid_mako',  # newly added
]

setup(
        name="template_app",
        install_requires=requires,
        entry_points="""\
        [paste.app_factory]
        main = template_app.app_config:main
        """,
)
