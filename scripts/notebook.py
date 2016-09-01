import argparse
import os
import shutil
import webbrowser


DOCS = os.path.normpath(
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "../docs"
            )
        )

def build_docs():
    print("Building Notebook...")
    os.system("cd {} && make html".format(DOCS))


def view_docs():
    print("Opening Notebook in web browser...")
    index_path = os.path.abspath(os.path.join(DOCS, "build", "html",
        "index.html"))
    index_url = "file://" + index_path
    webbrowser.open(index_url)
    print()


def destroy_build():
    print("Destroying previous build...")
    build_path = os.path.join(DOCS, "build")
    shutil.rmtree(build_path)


def main():
    args = parse_args()

    if args.rebuild is True:
        destroy_build()

    build_docs()

    if args.refresh is False:
        view_docs()


def parse_args():
    parser = argparse.ArgumentParser(description="Manipulte Notebook")
    parser.add_argument('--refresh', '-r',
            action="store_true", dest="refresh", default=False,
            help="Run sphinx-build but do not launch browser again.")
    parser.add_argument('--rebuild', '-d',
            action='store_true', dest="rebuild", default=False,
            help="Remove previous build before running sphinx-build.")
    return parser.parse_args()


if __name__ == "__main__":
    main()
