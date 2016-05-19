.. _ini_to_dict:

============
.ini to dict
============

If one ever desired turning a ``.ini`` file into a python dictionary (:ref:`perhaps
to run functional tests on a pyramid application <pyramid_functional_tests>`)
it's as easy as this!


.. code-block:: python

    def ini_to_dict(ini_path, sections=[]):
        """ convert ini options into dict """
        config = configparser.ConfigParser()
        config.read(ini_path)

        settings = defaultdict(lambda x: dict())
        for section in config.sections():
            if section in sections:
                for option in config.options(section):
                    settings[option] = config.get(section, option)

        return settings


If you're using a :ref:`pyramid` application and are doing this then the usage
would look something like this:


.. code-block:: python
    :emphasize-lines: 5

    global_config = {
            "__file__": "path/to/.ini",
            "here": "location/of/application",
            }
    settings = ini_to_dict("path/to/.ini", sections=["app:main_app"])
    app = app_config.main(global_config, **settings)
