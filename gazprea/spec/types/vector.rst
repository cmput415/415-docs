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
operators); and a vector of inferred-size arrays pads to the size of its
*first* element (see below), whereas a matrix literal pads to its longest
row (see :ref:`sssec:matrix_constr`).

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

The element type ``T`` of a ``vector<T>`` may be any
:ref:`storable type <ssec:storable_types>`: a base type (``boolean``,
``integer``, ``real``, ``character``), an array or matrix of any rank, a
``string``, a ``tuple``, a ``struct``, or another ``vector`` — nested to
any depth. Only a :ref:`stream <sec:streams>` may not be stored. Below
are some examples of ``vector`` declarations.
   
    ::

        const vector<integer[2]> v1 = 3;       // [[3, 3]]
        const vector<integer[2]> v2 = [4, 5];  // [[4, 5]]
        const vector<integer> v3 = 42;         // [42]
        var vector<integer> v4 = 42;           // [42], mutable
        vector<integer> v5 = 42;               // [42], implied const
        const vector<real> v6 = 1;             // [1.0]


Vectors of inferred-size arrays (``vector<T[*]>``) assume the shape of the
*first* array in the vector. Subsequent array elements shorter than the
inferred size are padded with the element type's :term:`zero value`; those
longer raise a :term:`run time` ``SizeError``. (Contrast with
:ref:`matrix construction <sssec:matrix_constr>`, where rows pad to the
*longest* row: the same nested literal can be legal as a matrix and a
``SizeError`` as a vector of arrays.)

A vector of arrays is therefore never ragged: every array element has the
same shape as the first element. A ``vector<vector<T>>``, by contrast,
*may* be ragged, because each inner vector carries its own runtime length
and no element imposes its shape on the others. This version of the
language has no broadcasting and no ``shape()`` operation.

   ::

        const vector<character> vec = ['a', 'b', 'c'];
        const vector<real[*]> ragged_right = [[1.0], [2.0, 2.0]]; // SizeError
        const vector<real[*]> padded_right = [[1.0, 2.0], [1.0]]; // Pads second element
        const vector<character> const_vec = vec;


Operations
~~~~~~~~~~~

Operations on vectors use the same syntax as operations on arrays and,
except for the differences enumerated above, share their semantics: in an
expression a vector is treated as an array value of its current length.
In particular, operand lengths must match for binary expressions and dot
product. All binary operations between a vector and an array produce
*array* results -- vector-ness is not propagated through operators.

.. _sssec:vec_methods:

Method Calls
~~~~~~~~~~~~

As a language-supported object, *Gazprea* provides methods for ``vector``
(and therefore for the typealias :ref:`string <ssec:string>`, which is just
``vector<character>``). A method call has the form
``receiver.method(arguments)`` and is governed by the following rules:

- A method call is defined as a procedure whose first parameter is the
  receiver. A method ``m(args)`` invoked on a ``vector<T>`` receiver
  behaves exactly as a call to
  ``procedure m(vector<T> self, args...) returns U``: the receiver is bound
  to ``self`` and the call has ordinary procedure-call semantics. Only
  ``vector`` (and thus ``string``, its typealias) has methods in this
  version of the language; user-defined methods on ``struct`` types are a
  future extension.

- The receiver must be a variable of a language-supported object type
  (``vector`` or ``string``). Arrays, array slices, and the (array-valued)
  results of expressions have no methods; calling a method on them is a
  compile-time ``TypeError``.

- A method call whose result is used is an expression. A method call may
  also stand alone as a statement, terminated by a semicolon; this is the
  only expression form that may be used as a statement. An explicit
  ``call`` statement may also be applied to a method call, but because the
  builtin methods act through the receiver, ``call m(...)`` is effectively
  a no-op form -- it behaves like calling a procedure and discarding its
  result.

- Mutating methods (``push``, ``append``) additionally require the
  receiver to be declared ``var``. Inside a :ref:`function <sec:function>`,
  mutating methods may be applied only to variables local to the function;
  this preserves function purity, since no state outside the function can
  change.

The methods are:

- ``push(T)`` - pushes a new element to the back of the vector, where ``T`` is the element type of the vector

- ``len()`` - number of elements in the vector

- ``append(x)`` - append to the vector, where ``T`` is the element type:
  if ``x`` is a single value implicitly castable to ``T`` it is cast to
  ``T`` and appended as a single element; otherwise ``x`` must be an array
  whose elements are each implicitly castable to ``T``, and its elements
  are appended in order. When both readings apply, the single-element
  reading is used.

   ::

        var vector<integer> v1;        // v1 == []
        v1.len() -> std_output;        // 0

        v1.push(1);                    // v1 == [1]
        v1.len() -> std_output;        // 1

        v1.push(2);                    // v1 == [1, 2]
        v1.len() -> std_output;        // 2

        v1.append([3, 4, 5])           // v1 == [1, 2, 3, 4, 5]
        v1.len() -> std_output;        // 5

        var vector<real[2]> v2;        // v2 == []
        const x = 1..10; 
        
        // `1` is implicitly cast to `[1.0, 1.0]` before appending
        v2.append(1);                  // v2 == [[1.0, 1.0]]

        // length 1 array padded to length 2
        v2.append([3.0]);              // v2 == [[1.0, 1.0], [3.0, 0.0]]               
        
        // slices
        v2.append(x[5..7]);            // v2 == [[1.0, 1.0], [3.0, 0.0], [5.0, 6.0]]

        v2.len() -> std_output         // 3

        v2.len();                      // Legal statement; result discarded

        (v1 + v1).push(3);             // TypeError: the sum is an array
                                       // value, and arrays have no methods

Slicing a vector produces an array slice (there are no "vector slices").

   ::

        // Slicing a vector produces an array slice
        vec[2..5].append(x[5..7])      // TypeError; cannot do `append` on an array slice
