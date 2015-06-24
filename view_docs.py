import os

# build the sphinx docs before running
# fabric/docs/buildpath
os.system("cd ./docs && make html")

# run sphinx with xdg
# fabric/docs/local_path
os.system("xdg-open ./docs/_build/html/index.html 2>&1 > /dev/null &")
