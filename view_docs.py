import argparse
import os


ROOT_DIR = os.path.dirname(__file__)


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
            help="Rebuild Notebook but do not launch xdg-open again.")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    build_docs()
    if args.refresh is not True:
        view_docs()
