from setuptools import setup

requires = [
        'pyramid',
        'pyramid_mako',
]

setup(
        name="bootstrap_form_app",
        install_requires=requires,
        entry_points="""\
        [paste.app_factory]
        main = bootstrap_form_app.setup_app:main
        """,
)
