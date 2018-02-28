Installation
============

The best way to install pyflightdata is via pip

.. code-block :: bash

    pip install pyflightdata

The dependencies will also be installed, however there have been issues with lxml.
You might need to install that separately and resolve installation issues. lxml is used
to parse data that is in pure HTML and does not provide a JSON data source.