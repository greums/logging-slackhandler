logging-slackhandler
====================

|Version| |Status| |Python| |License| |Build|

Introduction
------------

Python logging handler for Slack web hook integration with simple configuration.

Installation
------------

You can install, upgrade or uninstall logging-slackhandler with these commands:

.. code-block:: bash

    pip install logging-slackhandler
    pip install --upgrade logging-slackhandler
    pip uninstall logging-slackhandler

Usage
-----

The following example shows how to send message to a Slack Incoming Webhooks:

.. code-block:: python

    import logging
    from SlackLogger import SlackHandler, SlackFormatter

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    slack_handler = SlackHandler(YOUR_WEBHOOK_URL)
    slack_handler.setFormatter(SlackFormatter())

    logger.addHandler(slack_handler)

    logger.info('Hi there!')

License
-------

Copyright (c) 2017 Damien Le Bourdonnec

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

.. |Version| image:: https://img.shields.io/pypi/v/logging-slackhandler.svg?colorB=ee2269
    :target: https://pypi.python.org/pypi/logging-slackhandler
    :alt: Package Version
.. |Status| image:: https://img.shields.io/pypi/status/logging-slackhandler.svg
    :target: https://pypi.python.org/pypi/logging-slackhandler
    :alt: Development Status
.. |Python| image:: https://img.shields.io/pypi/pyversions/logging-slackhandler.svg?colorB=fcd20b
    :target: https://pypi.python.org/pypi/logging-slackhandler
    :alt: Python Version
.. |License| image:: https://img.shields.io/pypi/l/logging-slackhandler.svg
    :target: https://pypi.python.org/pypi/logging-slackhandler
    :alt: License
.. |Build| image:: https://img.shields.io/travis/Greums/logging-slackhandler.svg
    :target: https://travis-ci.org/Greums/logging-slackhandler
    :alt: Build Status
