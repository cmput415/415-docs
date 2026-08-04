Formatting
----------

Whitespace
~~~~~~~~~~

- Spaces are used to demarcate tokens in the language, although some keyword constructs may include spaces.

- Multiple spaces and tabs are treated as single spaces and are otherwise irrelevant.

- Indentation is irrelevant.

- A command starts at the beginning of a line and a newline indicates the end of a command, except in special cases.

- A newline will be Carriage Return (``'\r'`` or 0xd), a Line Feed (``'\n'`` or 0xa) or both (``'\r\n'``) depending on the implementing system. This is only in regards to LOLCODE code itself, and does not indicate how these should be treated in strings or files during execution.

- Multiple commands can be put on a single line if they are separated by a comma (``','``). In this case, the comma acts as a virtual newline or a soft-command-break.

- A single-line comment is always terminated by a newline. Soft-command-breaks (``','``) after the comment (``BTW``) are ignored.


Comments
~~~~~~~~

Single line comments are begun by ``BTW``, and may occur either after a line of code, on a separate line:

::

   HAI          BTW A single line comment
       VISIBLE "Hullo!"
                BTW Also a single line comment
   KTHXBYE

Multi-line comments are begun by ``OBTW`` and ended with ``TLDR``, and should be
started on their own lines, or following a line of code after a line separator.

These are valid multi-line comments:

::
   
    I HAS A VAR ITZ 12
            OBTW this is a long comment block
                 see, i have more comments here
                 and here
            TLDR
    I HAS A FISH ITZ BOB

::

    I HAS A VAR ITZ 12,  OBTW this is a long comment block
      see, i have more comments here
      and here
    TLDR, I HAS A FISH ITZ BOB
