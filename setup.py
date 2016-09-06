from setuptools import setup


setup_kwargs = {
        "name": "notebook",
        "version": "0.1",
        "url": "https://github.com/MaxwellGBrown",
        "entry_points": {
            "console_scripts": [
                "notebook = scripts.notebook:main",
                ],
            "sphinx_themes": [
                "path = sphinx_themes:get_path",
                ],
            },
        }


if __name__ == "__main__":
    setup(**setup_kwargs)
