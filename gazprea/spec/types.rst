.. _sec:types:

Types
=====

Type names appear in lower case as code (``string``, ``vector``,
``integer``); section titles use ordinary title capitalization.

.. toctree::
   :maxdepth: 2

   types/boolean
   types/character
   types/integer
   types/real
   types/tuple
   types/struct
   types/array
   types/vector
   types/string
   types/matrix

.. _ssec:storable_types:

Storable Types, Nesting, and Recursion
--------------------------------------

A *storable type* is any type whose values may be stored in a variable,
passed as an argument, returned, or held as a member of an
:term:`aggregate <aggregate type>`. Every type in *Gazprea* is storable
except :ref:`streams <sec:streams>`, which name I/O endpoints rather than
values.

Aggregates may be nested to any depth. An :ref:`array <ssec:array>` of any
rank (a :ref:`matrix <ssec:matrix>` is the rank-2 case), a
:ref:`vector <ssec:vector>`, a
:ref:`tuple <ssec:tuple>`, and a :ref:`struct <ssec:struct>` may each hold
any storable element or field type, including one another. For example a
``vector<S>`` (for a struct type ``S``), a struct with a ``tuple`` field,
and a ``tuple(S, integer[3][3])`` are all :term:`well-formed`.

Nesting must be **acyclic** through :term:`value types <value type>`. A
``struct`` or ``tuple`` whose fields, directly or transitively, contain a value
of its own type has no finite size and is :term:`ill-formed`; the compiler must
emit a ``TypeError`` (see :ref:`sec:errors`). A type may, however, refer to
itself *through a* :ref:`vector <ssec:vector>`, because a vector is dynamically
sized and stored by indirection:

::

     struct Tree (integer value, vector<Tree> children);  // well-formed
     struct Bad  (integer value, Bad next);               // TypeError: infinite size

.. note::

   *Implementation.* Nested aggregates are laid out and accessed
   structurally (a chain of ``getelementptr`` in the LLVM dialect); the
   vector at a recursion boundary is the sole point of indirection. Flat,
   non-nested sequences continue to lower through the tensor/linalg path,
   and should be implemented as contiguous blobs of memory, not lists of
   lists or structs of arrays pointing to arrays.
