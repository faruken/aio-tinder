.. image:: https://api.travis-ci.org/faruken/aio-tinder.svg
.. image:: https://img.shields.io/pypi/status/aio-tinder.svg
   :target: https://pypi.python.org/pypi/aio-tinder
   :alt: Development Status
.. image:: https://img.shields.io/codacy/grade/d8ea83742f744fe9afb7f7c9158b6154/master.svg
.. image:: https://api.codacy.com/project/badge/Grade/d8ea83742f744fe9afb7f7c9158b6154
    :target: https://www.codacy.com/app/alwayscocacola/aio-tinder?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=faruken/aio-tinder&amp;utm_campaign=Badge_Grade
.. image:: https://codeclimate.com/github/faruken/aio-tinder/badges/gpa.svg
   :target: https://codeclimate.com/github/faruken/aio-tinder
   :alt: Code Climate
.. image:: https://codeclimate.com/github/faruken/aio-tinder/badges/issue_count.svg
   :target: https://codeclimate.com/github/faruken/aio-tinder
   :alt: Issue Count


Introduction
************
This is a simple Tinder API for Python 3.5 and above.

Tinder API request/responses are captured with `mitmproxy <https://mitmproxy.org/>`_.


Note
====
This library is Python 3.5 and above only. It relies on asyncio and type hinting which are features available only in Python 3.5 and above henceforth the library is not compatible with the previous Python versions.


Installation
************

.. code-block:: bash

    $ pip install aio-tinder


Example
*******
There's an example code in `examples` folder to get the recommended users from Tinder with this library.
