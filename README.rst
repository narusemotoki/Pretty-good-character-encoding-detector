#######################################
Pretty good character encoding detector
#######################################

This library wrapped `chardet <https://github.com/chardet/chardet>`_.

===========
Basic usage
===========

::

    % ./pgced.py '{"sources": [{"type": "url", "uri": "http://google.com"}, {"type": "file", "uri": "pgced.py"}]}'
    [{"confidence": 1, "type": "url", "uri": "http://google.com", "encoding": "SHIFT_JIS"}, {"confidence": 1.0, "type": "file", "uri": "pgced.py", "encoding": "ascii"}]

======
Future
======

- Response include converted utf-8 characters.
- Speed with parallel access to uri.
- Bridge for other programming languages.
    - Now supporting
        - Python
    - Future
        - Go
        - PHP
