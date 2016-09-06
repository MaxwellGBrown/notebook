from os import path


sphinx_themes_dir = path.abspath(path.dirname(__file__))


def get_path():
    return sphinx_themes_dir
