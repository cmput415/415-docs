.. _ssec:tuple:

Tuples
------

A ``tuple`` is a way of grouping multiple values with potentially different types into an aggregate data structure. Tuples are similar to :ref:`structs<ssec:struct>`, except that a tuple's fields are indexed instead of named. Tuples are often used to return multiple values from a function or procedure. Any type may be stored within tuples except structs and tuples. Additionally streams can not be stored in tuples.

.. _sssec:tuple_decl:

Declaration
~~~~~~~~~~~

A tuple value is declared with the keyword ``tuple`` followed by a
parentheses-surrounded, comma-separated list of types. The list must
contain *at least two elements*. Tuples are *mutable*. For example:

::

     tuple(integer, real, integer[10]) t1;
     tuple(character, real, character[256], real) t2;

Note that while each tuple declaration defines a new type, the tuple type
is not named explcitly. Rather, it has a type *signature* ``(T1, T2, ...)``,
where ``T1, T2`` are the types of its members.
The number of fields in a ``tuple`` must be known at compile time.
This includes instances of :ref:`type inference<ssec:typeQualifiers_infer>`, where a variable is
declared without an explicit type signature using ``var`` or ``const``
.
In this case, the variable must be initialised immediately with a literal whose
type is known at compile time.

.. _sssec:tuple_acc:

Access
~~~~~~

The elements in a tuple are accessed using dot notation. Dot
notation can only be applied to tuple variables and *not* tuple literals.
Dot notation means an identifier followed by a period and then a literal
integer. Spaces are not allowed between elements in dot notation.
Field indices *start at one*, not zero. For example:

::

     t1.1
     t2.4

Tuple access can be used either to retrieve the element value for an expression
or to assign a new value to the element.

::

     y = x + t1.1;     // Allowed
     t1.1 = type-expr; // Allowed


.. _sssec:tuple_lit:

Literals
~~~~~~~~

A tuple literal is constructed by grouping values together between
parentheses in a comma separated list. For example:

::

     tuple(integer, character[5], integer[3])  my_tuple = (x, "hello", [1, 2, 3]);
     var my_tuple = (x, "hello", [1, 2, 3]);
     const your_tuple = (x, "hello", [1, 2, 3]);
     tuple(integer, real, integer[10]) tuple_var = (1, 2.1, [i in 1..10 | i]);

.. _sssec:tuple_ops:

Operations
~~~~~~~~~~

The following operations are defined on tuple values. In all of the
usage examples ``tuple-expr`` means some expression yielding tuples with the same type signature,
while ``int_lit`` is an integer literal as defined in :ref:`Integer Literals <sssec:integer_lit>` and ``tuple-inst`` is the
name of tuple instance as defined in :ref:`sec:identifiers`.

+------------+---------------+------------+------------------------------+-------------------+
| **Class**  | **Operation** | **Symbol** | **Usage**                    | **Associativity** |
+------------+---------------+------------+------------------------------+-------------------+
| Access     | dot           | ``.``      | ``tuple-inst.int_lit``       | left              |
+------------+---------------+------------+------------------------------+-------------------+
| Comparison | equals        | ``==``     | ``tuple-expr == tuple-expr`` | left              |
+            +---------------+------------+------------------------------+-------------------+
|            | not equals    | ``!=``     | ``tuple-expr != tuple-expr`` | left              |
+------------+---------------+------------+------------------------------+-------------------+

Note that in the above table ``tuple-expr`` may refer to a variable for access.
Accessing a literal could be replaced immediately with the scalar inside the tuple literal, however, ``tuple-expr`` may
refer to a literal in comparison operations to enable shorthand like this:

::

     if ((a, b) == (c, d)) { }

Comparisons are performed pairwise. Two tuples are equal when for every expression pair, the equality operator returns true.
Two tuples are unequal when one or more expression pairs are unequal or the types mismatch. This table describes how the
comparisons are completed, where ``t1`` and ``t2`` are tuple yielding expressions including literals:

============= =========================================
**Operation** **Meaning**
============= =========================================
``t1 == t2``  ``t1.1 == t2.1 and ... and t1.n == t2.n``
``t1 != t2``  ``t1.1 != t2.1 or ... or t1.n != t2.n``
============= =========================================


.. _sssec:tuple_unpack:

Unpacking
~~~~~~~~~

Any tuple expression may be assigned (unpacked) into multiple lvalues. If the size of
the tuple being unpacked does not match the number of lvalues being asigned, an ``AssignError``
may be raised. There is no partial unpacking of tuples.

::

    var real a;
    var real b;
    a, b = (3.14, 1.5);


Type Casting and Type Promotion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To see the types that tuple may be cast and/or promoted to, see the sections on :ref:`sec:typeCasting`
and :ref:`sec:typePromotion`, respectively.
