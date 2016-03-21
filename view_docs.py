import argparse
import os
import shutil


ROOT_DIR = os.path.dirname(__file__)


def destroy_build():
    """Destroys build so make gives full sphinx build errors"""
    print("Destroying previous build...\n")
    build_path = os.path.join(ROOT_DIR, "docs", "build")
    shutil.rmtree(build_path)


def build_docs():
    print("Builiding Notebook...\n")
    makefile_path = os.path.join(ROOT_DIR, "docs/")
    os.system("cd {} && make html".format(makefile_path))


def view_docs():
    print("Opening Notebook in web browser...")
    index_path = os.path.join(ROOT_DIR, "docs/build/html/index.html")
    os.system("xdg-open {} 2>&1 > /dev/null &".format(index_path))


def parse_args():
    parser = argparse.ArgumentParser(description="Open Notebook in Web Browser")
    parser.add_argument('--refresh', '-r',
            action="store_true", dest="refresh", default=False,
            help="Run sphinx-build but do not launch xdg-open again.")
    parser.add_argument('--rebuild', '-d',
            action='store_true', dest="rebuild", default=False,
            help="Remove previous build before running sphinx-build.")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    if args.rebuild is True:
        destroy_build()
    build_docs()
    if args.refresh is not True:
        view_docs()
