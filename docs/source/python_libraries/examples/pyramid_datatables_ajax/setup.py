from setuptools import setup

requires = [
        'pyramid',
]

setup(
        name="datatables_ajax_app",
        install_requires=requires,
        entry_points="""\
        [paste.app_factory]
        main = datatables_ajax_app.setup_app:main
        """,
)
