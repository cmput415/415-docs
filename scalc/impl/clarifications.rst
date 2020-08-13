Clarifications
==============

These clarifications are meant to add more information to the
specification without cluttering it.

#. 

   .. _clarify:no-rem:

   .. container::
      :name: no-rem

      **no-rem**:

   There is no remainder operator in SCalc. For example, the following
   tests would be considered invalid:

   ::

            int i = 5 % 2;

#. 

   .. _clarify:no-pow:

   .. container::
      :name: no-pow

      **no-pow**:

   There is no exponentiation operator in SCalc. For example, the
   following tests would be considered invalid:

   ::

            int i = 2 ^ 2;

#. 

   .. _clarify:int-div:

   .. container::
      :name: int-div

      **int-div**:

   Division is integer division. This means that any decimal portion of
   a division operation result is truncated (not rounded). No extra work
   is required: this is the default in C++, MIPS, ARM, and X86. For
   example:

   ::

            print(5 / 3);
            print((0 - 5) / 3);

   produces the following output:

   ::

            1
            -1

#. 

   .. _clarify:no-decl-cond:

   .. container::
      :name: no-decl-cond

      **no-decl-cond**:

   Declarations in conditionals can lead to undefined values due to
   global scoping. Because of the potentially conditional nature of the
   execution, it is possible to violate the property of variables
   stating that :ref:`variables must be defined before being used <variable-props>`
   (not just declared) by never executing the
   definition. For example, the following test would break this property
   and is therefore invalid:

   ::

            if (1 < 0)
              int i = 0;
            fi
            int j = i;

#. 

   .. _clarify:no-decl-loop:

   .. container::
      :name: no-decl-loop

      **no-decl-loop**:

   Declarations in loops can lead to undefined or repeatedly defined
   values due to global scoping. Because of the potentially conditional
   nature of the execution, it is possible to violate the property of
   variables stating that :ref:`variables must be defined before being used <variable-props>` (not just declared) by never executing the
   definition. For example, the following test would break this property
   and is therefore invalid:

   ::

            loop (1 < 0)
              int i = 0;
            pool
            int j = i;

   As well, because of the potentially repeated nature of the execution,
   it is possible to violate the property of variables stating that
   :ref:`variables can only be defined once <variable-props>` by repeating
   the declaration. For example, the following test would break this
   property and is therefore invalid:

   ::

            int i = 0;
            loop (i < 2)
              int j = 0;
              i = i + 1;
            pool;

#. 

   .. _clarify:empty-input:

   .. container::
      :name: empty-input

      **empty-input**:

   Empty input should result in empty output. This is in keeping with
   all of the output rules defined. There are no ``print`` statements so
   there would be no numbers, newlines or output of any kind. All that
   you are left with is a single empty line, which matches "*should* be
   an empty line at the end of your output".

