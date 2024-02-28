souper
======

This is my image crawler for `soup.io <http://www.soup.io/>`_

It generates a simple webpage with an image slideshow.

command line
------------

Main entry point is ``./run.py``

* for a complete list of options see ``./run.py --help``

* to configure logging use
    * ``-v`` or ``--verbosity`` to set the log level
* to configure output
    * ``--title`` to set the page title
* use ``--delay`` to configure the duration (in milliseconds)
  how long an image is displayed
* final two required arguments are the source and target folders


running
-------

Although the generated webpage is static, it won't work when not served
through a webserver.

JSON requests are not allowed on local files.

In doubt, change into the *www* folder, and use this command::

    python3 -m http.server 8000 --bind localhost

`localhost:8000 <http://localhost:8000>`_
