.. _sec:declaration:

Declarations
============

Variables must be declared before they are used. Aside from
a few :ref:`special cases <ssec:declaration_special>`, declarations have the
following formats:

::

       [<qualifier>] [<type>] <identifier> [= <expression>];

A declaration creates a variable with an :ref:`identifier <sec:identifiers>` of
``<identifier>``, with :ref:`type <sec:types>` ``<type>``, and optionally a
:ref:`type qualifier <sec:typeQualifiers>` of ``<qualifier>``. The two
qualifiers are ``var`` and ``const``, which qualify the identifier as *mutable*
or *immutable*, respectively. In *Gazprea* it is important to remember that if
the optional qualifier is omitted the default is ``const``, i.e. variables are
immutable by default (normative statement in :ref:`sec:typeQualifiers`).

Both ``<qualifier>`` and ``<type>`` are optional, but **at least one must be
present** so that the declaration can be told apart from an assignment. When
``<type>`` is elided it is inferred from ``<expression>``, which must therefore
be present and have an inferable type; if the type cannot be inferred the
compiler must emit a ``TypeError`` (see :ref:`sec:typeInference` and
:ref:`sec:errors`). When ``<qualifier>`` is elided it defaults to ``const`` as
described above.

Optionally, a declaration may explicitly initialize the value of the new
variable with the value of ``<expression>``.

In *Gazprea* all variables must be initialized in a well-defined manner in
order to ensure :term:`functional purity`. If the variables are not
initialized to a known value their initial value might change depending on
when the program is run.
*Gazprea* therefore follows a strict RAII-style discipline: every
declaration is also an :term:`initialization`, and no
variable is ever observable in an uninitialized state.  When the
programmer omits the explicit initializer, the compiler implicitly
initializes the variable to the :term:`zero value` of its type.
The zero value is ``0`` for ``integer``, ``0.0`` for ``real``,
``false`` for ``boolean``, ``'\0'`` (the null character) for ``character``, the
empty collection (e.g. the empty string ``""``) for a ``vector`` or
``string``, and, for a fixed-size :term:`aggregate type <aggregate type>`
(array, matrix, tuple, or struct), each element or field set to its own
zero value.
*Gazprea* has no ``null`` value.
An array's length is likewise settled at :term:`initialization` and is
then fixed for the remainder of the variable's lifetime (see
:ref:`sssec:array_sizing`): an uninitialized array holds its declared
number of elements, each set to the element type's zero value.
This applies to ``const`` declarations as well: a ``const`` variable
declared without an initializer is legal and holds the zero value of
its type permanently.

A declaration may appear at **any** point within a block; *Gazprea* does not
require the declarations of a block to be grouped at its start, so a declaration
may be interleaved freely with the statements around it. For instance, this is
legal even though a declaration follows an ordinary statement:

::

       var integer i = 10;
       if (blah) {
         i = i + 1;         // an ordinary statement
         var real r = 2.0;  // a declaration after a statement -- legal
         r = r + i;
       }

The one exception is :ref:`global scope <sec:global>`, where declarations are
**not** free to appear in any order: because every global is initialized before
the program runs, a global may reference only globals defined *earlier* in the
file, so globals must be written in :term:`initialization` order (see
:ref:`sec:global`).

A variable's name enters :term:`scope` only after its initializer has
been evaluated. A program that refers to a variable within its own
initialization statement is therefore :term:`ill-formed`.

::

       /* All of these declarations are illegal: the right-hand-side identifier
          is not yet in scope during its own initializer. */
       integer i = i;
       integer[10] v = v[1] * 2;

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
