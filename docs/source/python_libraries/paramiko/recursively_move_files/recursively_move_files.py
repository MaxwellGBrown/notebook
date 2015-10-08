import os
import stat

import paramiko

def get_filepaths_recursively(sftp, dir_path):
    for filepath in sftp.listdir(dir_path):
        if stat.S_ISDIR(sftp.stat(filepath).st_mode) is True:
            for subdir_filepath in get_files_recursively(filepath):
                yield os.path.join(filepath, subdir_filepath)
        else:
            yield filepath

def get_files_recursively(sftp, source_dir, destination):
    for remote_filepath in get_filepaths_recursively(sftp, source_dir):
        local_filepath = os.path.join(destination, remote_filepath)

        # make any dirs that don't exist yet
        if os.path.exists(os.path.dirname(local_filepath)) is False:
            os.makedirs(os.path.dirname(local_filepath))

        sftp.get(remote_filepath, local_filepath)

def main():

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname="localhost", username="johndoe", password="hunter2")
    
    sftp = ssh.open_sftp()
    get_file_recursively(sftp, "/foo/bar/", "~/Downloads")
