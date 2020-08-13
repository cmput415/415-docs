.. _sec:declaration:

Declarations
============

Variables must be declared before they are used. Aside from
a few :ref:`special cases <ssec:declaration_special>`, declarations have the 
following formats:

::

       <qualifier> <type> <identifier> = <expression>;
       <qualifier> <type> <identifier>;

Both declarations are creating a variable with an :ref:`identifier <sec:identifiers>` of
``<identifier>``, with :ref:`type <sec:types>` ``<type>``, and optionally a :ref:`type qualifier <sec:typeQualifiers>` of ``<qualifier>``.

The first declaration explicitly initializes the value of the new
variable with the value of ``<expression>``.

In *Gazprea* all variables must be initialized in a well defined manner
in order to ensure functional purity. If the variables were not
initialized to a known value their initial value might change depending
on when the program is run. Therefore, the second declaration is
equivalent to:

::

       <qualifier> <type> <identifier> = null;

For simplicity *Gazprea* assumes that declarations can only appear at
the beginning of a block. For instance this would not be legal in
*Gazprea*:

::

       integer i = 10;
       if (blah) {
         i = i + 1;
         real i = 0;  // Illegal placement of a declaration.
       }

because the declaration of the real version of ``i`` does not occur at
the start of the block.

The following declaration placement is legal:

::

       integer i = 10;
       if (blah) {
         real i = 0;  // At the start of the block. All good.
         i = i + 1;
       }

The declaration of a variable happens after initialization. Thus it is
illegal to refer to a variable within its own initialization statement.

::

       /* All of these declarations are illegal, they would result in garbage
          values. */
       integer i = i;
       integer v[10] = v[0] * 2;

An error message should be raised about the use of undeclared variables
in these cases. If a variable of the same name is declared in an
enclosing scope, then it is legal to use that in the initialization of a
variable with the same name. For instance:

::

       integer x = 7;
       if (true) {
         integer y = x;  /* y gets a value of 7 */
         real x = x; /* Refers to the enclosing scope's 'x', so this is legal */

         /* Now 'x' refers to the real version, with a value of 7.0 */
       }

.. _ssec:declaration_special:

Special cases
-------------

Special cases of declarations are covered in their respective sections.

#. :ref:`Vectors <sssec:vector_decl>`
#. :ref:`Matrices <sssec:matrix_decl>`
#. :ref:`Tuples <sssec:tuple_decl>`
#. :ref:`Globals <sec:global>`
#. :ref:`Functions <sec:function>`
#. :ref:`Procedures <sec:procedure>`