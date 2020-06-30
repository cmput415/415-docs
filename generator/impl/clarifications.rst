Clarifications
==============

These clarifications are meant to add more information to the
specification without cluttering it.

#. 

    .. _clarify:rem-not-mod:

   .. container::
      :name: rem-not-mod

      **rem-not-mod**:

   The ``%`` operator is remainder not modulus. Some languages (e.g.
   Python) define ``%`` as the modulus operator while others (e.g. C++)
   define it as remainder. Using the ``%`` operator in C++ is sufficient
   for this assignment. For example, using the following test:

   ::

            [i in 0..2 | (i - 9) % 3];

   The following output would be considered incorrect because modulus
   was used:

   ::

            0 1 2

   The following output would be considered correct because remainder
   was used:

   ::

            0 -2 -1

#. 

    .. _clarify:int-div:

   .. container::
      :name: int-div

      **int-div**:

   Division is integer division. This means that any decimal portion of
   a division operation result is truncated (not rounded). No extra work
   is required: this is the default in C++. For example:

   ::

            [i in 0..6 | i / 3];
            [i in 0..6 | (0 - i) / 3];

   produces the following output:

   ::

            0 0 0 1 1 1 2
            0 0 0 -1 -1 -1 -2

#. 

    .. _clarify:empty-input:

   .. container::
      :name: empty-input

      **empty-input**:

   Empty input should result in empty output. This is in keeping with
   all of the output rules defined. There are no generators so there
   would be no numbers, spaces, newlines or output of any kind. All that
   you are left with is a single empty line, which matches "*should* be
   an empty line at the end of your output".

