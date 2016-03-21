from fabric.api import run

env.hosts = ['localhost', '127.0.0.1']

def get_hostname():
    run("hostname")

def make_blank_file(file_name="blank_file.txt"):
    run("touch {}".format(file_name))

def do_both(echo):
    get_hostname()
    print echo
    make_blank_file()
