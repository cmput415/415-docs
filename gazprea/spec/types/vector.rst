.. _ssec:vector:

Vectors
-------

Vectors are language-supported objects that provide runtime-sized arrays.
Unlike an array, whose length is fixed once at its :term:`initialization`
(see :ref:`sssec:array_vs_vector`), a vector is *runtime sized*: it begins
at some length and may grow over its lifetime through its mutating methods
(``push`` and ``append``).

Once created, ``vectors`` in *Gazprea* interoperate with arrays for the
element types they both support: they can be intermixed with arrays in
expressions; they can be used on the RHS of array declarations and
initializations; and they can be passed as array arguments to functions
and procedures. When a vector appears in an expression it is used as an
array value of its *current* length. Vectors are nevertheless a distinct
type, and the differences include (non-exhaustively): vectors have methods
where arrays have none; a mixed binary operation between a vector and an
array produces an *array* result (vector-ness is not propagated through
operators); and a ``vector<T[*]>`` (a vector of
inferred-size arrays) fixes its element size once, from the first array value
stored into it, and fits every later element to that size (see below).

.. _sssec:vec_decl:

Declaration
~~~~~~~~~~~

Vectors are declared and (optionally) initialized as follows.
(Note that we have replaced ``<>`` with ``|`` in the notation below since
the literals ``<`` and ``>`` are used in the declaration)

   ::

            [<qualifier>] vector<|type|> |identifier|;
            [<qualifier>] vector<|type|> |identifier| = |type-expr|;
            [<qualifier>] vector<|type|> |identifier| = |type-array|;


Unlike the array type, *Gazprea* vectors do not have an explicit size
specifier, often called *capacity* in other languages.

The element type ``T`` of a ``vector<T>`` may be any :ref:`storable type
<ssec:storable_types>`: a :term:`primitive type <primitive type>` (``boolean``,
``integer``, ``real``, ``character``), an array of any rank (a matrix is the
rank-2 case), a ``string``, a ``tuple``, a ``struct``, or another ``vector`` —
nested to any depth. Only a :ref:`stream <sec:streams>` may not be stored.
Below are some examples of ``vector`` declarations.

    ::

        const vector<integer[2]> v1 = 3;       // [[3, 3]]
        const vector<integer[2]> v2 = [4, 5];  // [[4, 5]]
        const vector<integer> v3 = 42;         // [42]
        var vector<integer> v4 = 42;           // [42], mutable
        vector<integer> v5 = 42;               // [42], implied const
        const vector<real> v6 = 1;             // [1.0]


A ``vector<T[*]>`` -- a vector whose element is an inferred-size array -- fixes
that element size (the ``*``) exactly once, from the **first array value that
enters the vector**, and fits every later element to it: a shorter array is
padded with the element type's :term:`zero value`, and a longer one raises a
``SizeError`` (see :ref:`sec:errors`). What counts as the "first value" depends
on how the vector is populated, and the two paths must not be conflated:

- **Initialized from an array value** (including a nested array *literal*): the
  right-hand side is evaluated to an array *value* on its own first, and only
  then stored. A nested literal such as ``[[1.0], [2.0, 3.0]]`` is an ordinary
  array literal, so it is normalized to a rectangle by padding every sub-array
  to the **longest** one -- exactly as in :ref:`matrix construction
  <sssec:matrix_constr>` -- *before* the vector ever sees it. This padding is a
  property of the literal, so it is identical whether the literal initializes an
  array variable or a vector.

- **Built up incrementally** with ``push`` / ``append`` from a shorter or empty
  vector: the elements arrive one at a time, so the **first** element stored
  fixes the size and each later element is fitted to it.

A vector of arrays is therefore never ragged: once the element size is fixed,
every element has that shape. A ``vector<vector<T>>``, by contrast, *may* be
ragged, because each inner vector carries its own runtime length and no element
imposes its shape on the others. This version of the language has no
broadcasting and no ``shape()`` operation.

Because a nested literal is padded to its longest sub-array before it is stored,
neither initializer below is ragged and neither is an error -- the short
sub-array is simply padded, whichever side it is on:

   ::

        const vector<character> vec = ['a', 'b', 'c'];       // ['a', 'b', 'c']

        // Each RHS is normalized to its longest sub-array, then stored:
        const vector<real[*]> x = [[1.0], [2.0, 3.0]]; // x == [[1.0, 0.0], [2.0, 3.0]]
        const vector<real[*]> w = [[1.0, 2.0], [1.0]]; // w == [[1.0, 2.0], [1.0, 0.0]]

        const vector<character> const_vec = vec;             // copy of vec

Growing a vector one element at a time is different: there is no surrounding
literal to normalize, so the first stored element fixes the size and each later
element is fitted to it. This is why the same value pads differently depending
on the path -- ``x`` above is padded as a whole literal, whereas ``y`` below
pads only its newly pushed element:

   ::

        var vector<real[*]> y = [[1.0, 2.0]]; // element size fixed at 2
        call y.push([3.0]);                   // [3.0] padded to [3.0, 0.0]
                                              // y == [[1.0, 2.0], [3.0, 0.0]]

An initially empty ``vector<T[*]>`` takes its element size from the first array
appended, after which the usual pad / ``SizeError`` rules apply. Each call below
is shown for its own effect on the freshly emptied vector:

   ::

        var vector<integer[*]> z;      // empty; element size not yet fixed
        call z.append([1, 2]);         // first element fixes the size at 2: z == [[1, 2]]
        call z.append([1]);            // shorter: padded to [1, 0]
        call z.append([1, 2, 3]);      // longer than the fixed size 2: SizeError
        call z.append(1);              // scalar 1 broadcasts to [1, 1], then appended


.. _sssec:vec_ops:

Operations
~~~~~~~~~~~

Operations on vectors use the same syntax as operations on arrays and,
except for the differences enumerated above, share their semantics: in an
expression a vector is treated as an array value of its current length.
In particular, operand lengths must match for binary expressions and dot
product. Every binary operation with a vector operand -- whether the
other operand is a vector or an array, and **including concatenation with**
``||`` -- produces an *array* result; vector-ness is never propagated through
operators. The resulting array may of course be implicitly cast back to a
vector (or ``string``) when it is stored into one (see
:ref:`ssec:implicitCasts_avv`), but that is a separate implicit cast, not a
property of the operator.

Operator precedence and associativity are specified once, for all types, in
the :ref:`table of operator precedence <ssec:expressions_toop>`.

.. _sssec:vec_methods:

Method Calls
~~~~~~~~~~~~

As a language-supported object, *Gazprea* provides methods for ``vector``
(and therefore for the typealias :ref:`string <ssec:string>`, which is just
``vector<character>``). A method call has the form
``receiver.method(arguments)`` and is governed by the following rules:

- Each method is either a :ref:`function <sec:function>` or a
  :ref:`procedure <sec:procedure>`, according to whether it observes the
  receiver or mutates it. A *stateless*
  method such as ``len`` is a **function**: it is pure, returns a value, and
  does not change the receiver. A *stateful* method such as ``push`` or
  ``append`` is a **procedure**: it mutates the receiver. A method ``m(args)``
  invoked on a ``vector<T>`` receiver behaves exactly as a call to
  ``function m(vector<T> self, args...) returns U`` (stateless) or
  ``procedure m(var vector<T> self, args...)`` (stateful): the receiver is
  bound to ``self`` and the call has ordinary function- or procedure-call
  semantics. Only ``vector`` (and thus ``string``, its typealias) has methods
  in this version of the language; user-defined methods on ``struct`` types
  are a future extension.

- The receiver must be a variable of a language-supported object type
  (``vector`` or ``string``). Arrays, array slices, and the (array-valued)
  results of expressions have no methods; calling a method on them is a
  :term:`compile time` ``TypeError`` (see :ref:`sec:errors`).

- A **function** method (such as ``len``) is an expression: its result is a
  value, so it may appear in any expression position -- on the right of a
  declaration or assignment, as an argument, or in an output-stream
  expression such as ``v.len() -> std_output``. Like any function call it may
  not stand alone as a statement, and ``call`` does not apply to it.

- A **procedure** method (such as ``push`` and ``append``) is used as a
  statement and, like any other
  :ref:`procedure call <ssec:procedure_call_positions>`, must be written as a
  ``call`` statement: ``call v.push(1);``. Written without the ``call``
  keyword -- a bare ``v.push(1);`` -- it is a :ref:`CallError <sec:errors>`.

- Mutating methods (``push``, ``append``) additionally require the
  receiver to be declared ``var``. Inside a :ref:`function <sec:function>`,
  mutating methods may be applied only to variables local to the function;
  this preserves function purity, since no state outside the function can
  change.

The methods are:

- ``push(T)`` (procedure) - pushes a new element to the back of the vector,
  where ``T`` is the element type of the vector

- ``len()`` (function) - number of elements in the vector

- ``append(x)`` (procedure) - append to the vector, where ``T`` is the element
  type: if ``x`` is a single value implicitly castable to ``T`` it is cast to
  ``T`` and appended as a single element; otherwise ``x`` must be an array
  whose elements are each implicitly castable to ``T``, and its elements are
  appended in order. When both readings apply, the single-element reading is
  used.

   ::

        var vector<integer> v1;        // v1 == []
        v1.len() -> std_output;        // 0

        call v1.push(1);               // v1 == [1]
        v1.len() -> std_output;        // 1

        call v1.push(2);               // v1 == [1, 2]
        v1.len() -> std_output;        // 2

        call v1.append([3, 4, 5]);     // v1 == [1, 2, 3, 4, 5]
        v1.len() -> std_output;        // 5

        var vector<real[2]> v2;        // v2 == []
        const x = 1..11;

        // `1` is implicitly cast to `[1.0, 1.0]` before appending
        call v2.append(1);             // v2 == [[1.0, 1.0]]

        // length 1 array padded to length 2
        call v2.append([3.0]);         // v2 == [[1.0, 1.0], [3.0, 0.0]]

        // slices
        call v2.append(x[5..7]);       // v2 == [[1.0, 1.0], [3.0, 0.0], [5.0, 6.0]]

        v2.len() -> std_output;        // 3

        call (v1 + v1).push(3);        // TypeError: the sum is an array
                                       // value, and arrays have no methods

Slicing a vector produces an array slice (there are no "vector slices").

   ::

        var vector<integer> v3 = x;
        call v3[2..5].append(x[5..7]); // TypeError; cannot do `append` on an array slice
