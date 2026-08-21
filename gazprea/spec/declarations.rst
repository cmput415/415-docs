.. _sec:declaration:

Declarations
============

Variables must be declared before they are used. Aside from
a few :ref:`special cases <ssec:declaration_special>`, declarations have the 
following formats:

::

       [<qualifier>] <type> <identifier> [= <expression>];

A declaration creates a variable with an :ref:`identifier <sec:identifiers>` of
``<identifier>``, with :ref:`type <sec:types>` ``<type>``, and optionally a :ref:`type qualifier <sec:typeQualifiers>` of ``<qualifier>``.
The two qualifiers are ``var`` and ``const``, which qualify the identifier as
*mutable* or *immutable*, respectively.
In *Gazprea* it is important to remember that if the optional qualifier is
omitted the default is ``const``, i.e. variables are immutable by default
(normative statement in :ref:`sec:typeQualifiers`).

Optionally, a declaration may explicitly initialize the value of the new
variable with the value of ``<expression>``.

In *Gazprea* all variables must be initialized in a well defined manner in
order to ensure :term:`functional purity`. If the variables are not
initialized to a known value their initial value might change depending on
when the program is run.
*Gazprea* therefore follows a strict RAII-style discipline: every
declaration is also an :term:`initialization <initializer>`, and no
variable is ever observable in an uninitialized state.  When the
programmer omits the explicit initializer, the compiler implicitly
initializes the variable to the :term:`zero value` of its type.
The zero value is ``0`` for ``integer``, ``0.0`` for ``real``,
``false`` for ``boolean``, ``' '`` (a space) for ``character``,
the empty string ``""`` for ``string``, and, for
:term:`aggregate types <aggregate type>` (arrays, vectors, tuples,
structs), each element or field set to its own zero value.
*Gazprea* has no ``null`` value.
An array's length is likewise settled at :term:`initialization` and is
then fixed for the remainder of the variable's lifetime (see
:ref:`sssec:array_sizing`): an uninitialized array holds its declared
number of elements, each set to the element type's zero value.
This applies to ``const`` declarations as well: a ``const`` variable
declared without an initializer is legal and holds the zero value of
its type permanently.

For simplicity *Gazprea* assumes that declarations can only appear at
the beginning of a block. For instance this would not be legal in
*Gazprea*:

::

       var integer i = 10;
       if (blah) {
         i = i + 1;
         real i = 0;  // Illegal placement of a declaration.
       }

because the declaration of the real version of ``i`` does not occur at
the start of the block. The compiler must emit a ``StatementError`` for
any declaration that appears after the declaration prefix at the start of
its enclosing block statement.

The following declaration placement is legal:

::

       var integer i = 10;
       if (blah) {
         var real i = 0;  // At the start of the block. All good.
         i = i + 1;
       }

The declaration of a variable happens after initialization. A program
that refers to a variable within its own initialization statement is
therefore :term:`ill-formed`.

::

       /* All of these declarations are illegal, they would result in garbage values. */
       integer i = i;
       integer[10] v = v[0] * 2;

The compiler must emit a ``SymbolError`` (see :ref:`sec:errors`) for the
use of undeclared variables in these cases. If a variable of the same name
is declared in an enclosing :term:`scope`, then it is legal to use that in
the initialization of a variable with the same name. For instance:

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

#. :ref:`Arrays <sssec:array_decl>`
#. :ref:`Matrices <sssec:matrix_decl>`
#. :ref:`Tuples <sssec:tuple_decl>`
#. :ref:`Globals <sec:global>`
#. :ref:`Functions <sec:function>`
#. :ref:`Procedures <sec:procedure>`
