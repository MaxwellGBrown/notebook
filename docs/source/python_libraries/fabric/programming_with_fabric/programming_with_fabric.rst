.. _programming_with_fabric:

============================
Using fabric programatically
============================

Although ``fabric`` was made for system admin tasks, it can be leveraged programatically in code. There are some hurdles to jump and it often isn't perfect, butfabric's ease of use can keep your high level code very clean.

------------------------------
Leveraging fabric.api.settings
------------------------------

To contextualize a connection to a server, we can use ``fabric.api.settings``. Normally ``settings`` is used to override the ``env`` dictionary in the fabfile which dictates our ``fabric``'s connection. We can use ``settings`` to supply connection settings when we never intended to leverage the ``env`` dictionary from the start.

::

    import fabric
    from fabric.api import settings, hide, run

    ssh_credentials = {
            "host_string": "remotehost.com",
            "user": "remote_user",
            "password": "hunter2",
            "abort_on_prompts": True,  # prompts will suspend program run
            "no_keys": True,  # we're authenticating with password, not keys
            "no_agent": True,  # no user agent
    }
    with settings(**ssh_credentials), hide('everything'):
        output = run("echo 'Hello World'")

In the above example, we're providing the connection settings as a ``**kwargs`` dictionary to ``fabric.api.settings`` and using ``fabric.api.hide`` to hide the stdout and sterr output from hitting our terminal. 

Everything done in the context of ``with settings(**ssh_credentials):`` will retain the same connection settings.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A note about fabric's lazy connections
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``fabric`` leverages "lazy connections". This meaning, if we do set up a ``fabric.api.settings`` object and use it to contextualize our actions, we aren't starting a connection to the server for the following commands to run using. **A server connection is only created when there is action to be taken, and after that action is created the connection is destroyed.**

Under normal circumstances, this isn't an issue. But if the remote server's shell settings leave an unavoidable "Message of the Day", that is going to be showing up in your stdout, and any assignment based on server response. 

For instance, if you're trying to verify the creation of a file, and the remote server has a "Message of the Day" informing you of your inbox status, **you will get that message in the output of every command**. 

Below is an example:

::

    with settings(**ssh_credentials):
        output1 = run("ls")
        output2 = run("touch newfile")
        output3 = run("ls")
        print(output1)  # >>> "No new mail!\r\n .. ."
        print(output2)  # >>> "No new mail!\r\n"
        print(output3)  # >>> "No new mail!\r\n .. . newfile"


So far, the only known way to alleviate this is to change the shell settings on the remote host. If you can count on the "Message of the Day" being consistant (like if there's no email set up for the user) then there are quick/dirty workarounds you can use to clean your output.

::

   clean_output = lambda x: "\r\n".join(x.split('\r\n')[1:]) 

... which just removes the first line of output ``"No new mail!\r\n"``
