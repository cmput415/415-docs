.. _sec:comments:

Comments
========

*Generator* supports a subset of *C99* comments.

Single line comments are made using ``//``. Anything on the line after
the two adjacent forward slashes is ignored. For example:

::

 // A comment on its own line
 [i in 1..10 | i * i];  // This is ignored
