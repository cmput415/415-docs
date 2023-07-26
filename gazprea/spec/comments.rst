.. _sec:comments:

Comments
========

*Gazprea* supports *C99* style comments.

Single line comments are made using ``//``. Anything on the line after
the two adjacent forward slashes is ignored. For example:

::

   	integer x = 2 * 3;  // This is ignored

Multi-line block comments are made using **/\*** and **\*/**. The start
of a block comment is marked using **/\***, and the end of the block
comment is the **first** occurrence of the sequence of characters
**\*/**. For example:

::

	/* This is a block comment. It can span as many lines as we want, and
	   only ends when the closing sequence is encountered.
   	 */
   	integer x = 2 * 3;  /* Block comments can also be on a single line */

Block comments cannot be nested because the comment finishes when it
reaches the first closing sequence. For example, this is invalid:

::

     /* A comment /* A nested comment */ */
