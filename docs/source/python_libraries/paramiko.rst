========
paramiko
========

paramiko is an SSH package for python. Use it to SSH into things.

.. toctree::
  :maxdepth: 1

  examples/paramiko_recursively_move_files/paramiko_recursively_move_files

 
Quickstart
----------

.. code-block:: python

  import paramiko
  ssh = paramiko.SSHClient()
  ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  ssh.connect('localhost', username="JonDoe", password="hunter2")
  
  stdin, stdout, stderr = ssh.exec_command("echo 'Hello World'")
  print(stdout.readlines())  # or stdout.read()

 
``stdin``, ``stdout``, and ``stderr`` are all file-like objects that are SSH channels to the respective machines input, output, and error channles.
