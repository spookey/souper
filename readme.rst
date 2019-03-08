souper
======

This is my image crawler for `soup.io <http://www.soup.io/>`_

It generates a simple webpage with an image slideshow.

command line
------------

Main entry point is ``./run.py``

* for a complete list of options see ``./run.py --help``

* to configure logging use
    * ``-l`` or ``--log`` to set the output folder for the logfiles
    * ``-v`` or ``--verbosity`` to set the log level
      (a debug logfile is always created)
* to configure output files use
    * ``-w`` or ``--www`` to set the root folder for generated files
    * ``--asset`` to rename the folder (within the root folder) for images
    * ``--store`` to set the filename which tracks the images
    * ``--index`` to rename the index.html
    * ``--style`` to rename the style.css
    * ``--logic`` to rename the logic.js
* use ``--delay`` to configure the duration (in milliseconds)
  how long an image is displayed

* use ``-p`` or ``--pages`` to stop crawling after some pages
  (0 - the default - will crawl until you've reached the end)

A username is always required.

running
-------

Although the generated webpage is static, it won't work when not served
through a webserver.

JSON requests are not allowed on local files.

In doubt, change into the *www* folder, and use this command::

    python3 -m http.server 8000 --bind localhost

`localhost:8000 <http://localhost:8000>`_
