import os


ROOT_DIR = os.path.dirname(__file__)


def build_docs():
    # build the sphinx docs before running
    makefile_path = os.path.join(ROOT_DIR, "docs/")
    os.system("cd {} && make html".format(makefile_path))


def view_docs():
    # run sphinx with xdg on built files
    index_path = os.path.join(ROOT_DIR, "docs/build/html/index.html")
    os.system("xdg-open {} 2>&1 > /dev/null &".format(index_path))


if __name__ == "__main__":
    build_docs()
    view_docs()
