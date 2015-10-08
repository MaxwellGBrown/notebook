========================
Recursively Move Files
========================

This example shows how to move a tree of files recursively from a remote host to the local host using paraiko's SFTP client.

.. literalinclude:: recursively_move_files.py
    :language: python
    :caption: recursively_move_files.py


``get_filepaths_recursively()`` is the function that recursively yields each file and subfile in the desired remote directory. Using sftp.stat (which imitates os.stat's functionality), it determines whether the filepath is a directory or a file. If it's a directory, it runs itself recursively.

``get_files_recursively()`` takes all the files gathered from ``get_filepaths_recursively()`` and saves them in the same structure to the ``destination`` filepath. It also handles the creation of any directories that don't currently exist, but exist inside the desired tree.

In ``main()``, an SFTPClient is created using the SSHClient's method ``open_sftp()``.
