.. _sec:value_categories:

Value Categories
================

Every expression in *Gazprea* belongs to exactly one **value category**,
which determines how the expression may be used. In essence, value categories
describe whether an expression
can appear on the left-hand side of an assignment and whether it can be passed
as a mutable (``var``) argument to a procedure.

*Gazprea* recognises two value categories: **lvalue** and **rvalue**. This is
a deliberate simplification of the richer taxonomy found in modern C++ (which
adds *xvalue*, *prvalue*, and *glvalue*); those additional categories exist to
support move semantics and resource transfer, neither of which *Gazprea*
exposes. The two-category model is sufficient for *Gazprea*'s ownership rules,
which are entirely copy-based.

The full C++ taxonomy is described at
`cppreference: Value categories <https://en.cppreference.com/w/cpp/language/value_category.html>`_
and is worth understanding as background, even if *Gazprea* does not expose all
of it.

.. _ssec:vc_background:

Background: The Full C++ Taxonomy
----------------------------------

C++ characterises expressions along two orthogonal axes:

- **Identity**: does the expression refer to a persistent object that has an
  address and can be named again later?
- **Moveability**: can the object's resources be transferred (moved) rather
  than copied?

This gives rise to five named categories, arranged in the following hierarchy:

.. code-block:: text

    Expression
    ├── glvalue  (has identity)
    │   ├── lvalue   (identity, not moveable)
    │   └── xvalue   (identity, moveable — "expiring value")
    └── rvalue   (may be moved from)
        ├── xvalue   (shared with glvalue above)
        └── prvalue  (no identity — "pure rvalue")

**glvalue** ("generalised lvalue")
    Any expression that determines the identity of an object or function.
    Includes both lvalues and xvalues. A glvalue *may* be implicitly converted
    to a prvalue.

**lvalue**
    A glvalue that is not an xvalue. Refers to a persistent object with a
    stable address — something you can take the address of and use again next
    time the same expression is evaluated. Variable names, array element
    accesses, and dereferenced pointers are classic lvalues.

**xvalue** ("expiring value")
    A glvalue whose resources can be reused because the object is near the end
    of its lifetime. Introduced in C++11 to support ``std::move`` and rvalue
    references. *Gazprea* has no equivalent.*

**prvalue** ("pure rvalue")
    An rvalue that is not an xvalue. Computes a value or initialises an object
    but has no persistent identity of its own. Literals, arithmetic
    sub-expressions, and function return values (when returned by value) are
    prvalues.

**rvalue**
    The union of xvalues and prvalues, anything that is not a glvalue.
    rvalues can generally be moved from (in C++) and cannot be the target of an
    ordinary assignment.

.. _ssec:vc_gazprea:

Value Categories in Gazprea
-----------------------------

Because *Gazprea* has no move semantics or reference types, xvalues never
arise. The two remaining categories collapse cleanly:

**lvalue**
    An expression that refers to a named, addressable storage location that
    persists beyond the expression and can appear on the left-hand side of an
    assignment. In *Gazprea*:

    - Named variables (``x``, ``arr``, ``my_tuple``)
    - Individual element accesses on mutable arrays (``arr[i]``, ``mat[i, j]``,
      ``tup.1``, ``tup.name``)

**rvalue**
    An expression that produces a value but has no persistent, named storage
    location. In *Gazprea*, rvalues correspond to what C++ would call
    *prvalues*:

    - Literals (``42``, ``true``, ``'a'``, ``"hello"``)
    - Arithmetic and logical sub-expressions (``x + 1``, ``a and b``)
    - Array and tuple literals (``[1, 2, 3]``, ``(x: 1, y: 2)``)
    - Range expressions (``1..10``)
    - **Slice expressions** (``arr[2..5]``) — even though slices are derived
      from a named array, the result is a fresh deep copy with no stable
      address of its own
    - Function call results

.. _ssec:vc_consequences:

Practical Consequences
-----------------------

The value category of an expression determines what you can do with it:

+---------------------------------------------+----------+---------+
| Operation                                   | lvalue   | rvalue  |
+=============================================+==========+=========+
| Appear on left-hand side of ``=``           | ✓        | ✗       |
+---------------------------------------------+----------+---------+
| Pass as ``var`` (mutable) procedure argument| ✓        | ✗       |
+---------------------------------------------+----------+---------+
| Pass as ``const`` procedure argument        | ✓        | ✓       |
+---------------------------------------------+----------+---------+
| Use in an expression                        | ✓        | ✓       |
+---------------------------------------------+----------+---------+

In particular, because a slice is an rvalue, the following are both
compile-time errors:

::

    var integer[5] a = [10, 20, 30, 40, 50];

    a[1..3] = [99, 99];       // ERROR: slice is an r-value, not an l-value

    procedure mutate(var integer[*] v) { ... }
    call mutate(a[1..3]);     // ERROR: cannot pass r-value as var argument
