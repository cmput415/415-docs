.. _ssec:vector:

Vectors
-------

Vectors are language supported objects that provide a **runtime sized**
collection. Unlike an :ref:`array <ssec:array>`, whose length is fixed once at
elaboration and never changes, the length of a vector is a property of its
current value: it is established when the vector is assigned to and it changes
whenever the vector is grown with ``push`` or ``append``.

A vector participates in array expressions by *yielding an array value* of its
current length — this is what the spec means when it says a vector can be used
as, or sliced into, an array. Specifically, a vector may be:

-  used in expressions wherever an array of its current length and element type
   would be legal;

-  used on the RHS of an array declaration, initialization, or assignment,
   subject to the usual :ref:`padding and SizeError rules <sssec:array_decl>`
   for the fixed length of the array on the LHS;

-  passed as an array argument to a function or procedure.

What a vector never does is make an array resizable, and what an array context
never does is fix a vector's length. The conversion is between *values*, in one
direction at a time; see :ref:`sssec:array_vs_vector` for the side-by-side
comparison.

.. _sssec:vec_decl:

Declaration
~~~~~~~~~~~

Vectors are declared and (optionally) initialized as follows.
(Note that we have replaced ``<>`` with ``|`` in the notation below since
the literals ``<`` and ``>`` are used in the declaration)

   ::

            vector<|type|> |identifier|;
            vector<|type|> |identifier| = |type-expr|;
            vector<|type|> |identifier| = |type-array|;


A vector type never carries a length: there is no ``vector<integer>[N]``, and
the ``[N]`` / ``[*]`` notation of arrays has no vector counterpart. The number
of elements a vector holds is not part of its type at all, which is precisely
why it is free to change at runtime. Below are some examples of ``vector``
declarations.

    ::

        const vector<integer[2]> v1 = 3;       // [[3, 3]]
        const vector<integer[2]> v2 = [4, 5];  // [[4, 5]]
        const vector<integer> v3 = 42;         // [42]
        const vector<real> v4 = 1;             // [1.0]

A vector declared without an initializer starts empty, rather than being
zero-filled to some length the way an array is. This is the vector analogue of
the rule in :ref:`sec:declaration` that an uninitialized variable takes its
zero value; for a runtime-sized collection the zero value is the empty vector.

    ::

        var vector<integer> v;   // [] -- length 0, but free to grow
        var integer[3] a;        // [0, 0, 0] -- length 3, forever

Note that the *element type* of a vector is still subject to array sizing
rules. Vectors of inferred sized arrays assume the size of the *first* array in
the vector, and that element size is then fixed for the lifetime of the vector
exactly as an array's own length would be — only the number of elements in the
vector remains free to change.
Subsequent array elements of less than the inferred size are padded.
Those greater raise a runtime ``SizeError``.

   ::

        const vector<character> vec = ['a', 'b', 'c'];
        const vector<real[*]> ragged_right = [[1.0], [2.0, 2.0]]; // SizeError
        const vector<real[*]> padded_right = [[1.0, 2.0], [1.0]]; // Pads second element
        const vector<character> const_vec = vec;


Operations
~~~~~~~~~~~

Operations on vectors are identical syntactically and semantically to
operations on arrays: in an expression, a vector is used as an array value of
its current length. In particular, operand lengths must match for binary
expressions and dot product, and the result of such an expression is an
*array*, not a vector — the vector-ness is not propagated through operators.
The lengths involved are the lengths the vectors happen to have when the
expression is evaluated:

   ::

      var vector<integer> v1;
      var vector<integer> v2;
      var integer[3] a;      // fixed at length 3 by this declaration

      v1.append([1, 2, 3]);  // v1 currently has length 3
      a = v1;                // legal: v1 yields a length-3 array value
      v2 = v1 + a;           // array result; v2 takes on length 3
      a = v1 + v2;           // array result of length 3, matches 'a'

      v1.push(4);            // v1 now has length 4 -- vectors are runtime sized
      a = v1;                // SizeError: 'a' is still length 3
      v2 = v1;               // fine: v2 takes on length 4

Assigning to an array and assigning to a vector are therefore *not*
symmetrical. Assigning into the array ``a`` must respect the length ``a`` was
elaborated with, and pads or raises a ``SizeError`` accordingly. Assigning into
the vector ``v2`` simply replaces its contents, length included.

A vector or vector slice can be passed as a call argument that has been
declared as an array of the same size and type; the check that the vector's
current length matches the parameter's declared length happens at the call.
When indexing a vector of arrays,
the first index selects the array element within the vector, and the second index selects
the element within the array:

 ::

        vector<real[*]> ragged_right = [[1.0], [2.1]];
        length(ragged_right[1]) -> std_output; // prints 1
        ragged_right[2][1] -> std_output; // prints 2.1


As a language supported object, *Gazprea* provides several methods for
``vector``. These are the operations that make a vector runtime sized; none of
them has an array counterpart, and applying the idea to an array — trying to
lengthen it — is always a ``SizeError``.

- ``push(T)`` - pushes a new element to the back of the vector, increasing its
  length by one. ``T`` is the element type of the vector, or a type that can be
  implicitly converted to it.

- ``len()`` - the number of elements the vector currently holds. This is the
  same value the :ref:`length <ssec:builtIn_length>` built-in reports for the
  same vector; ``len`` is the method spelling and ``length`` the built-in
  spelling.

- ``append(T[*])`` - append another array slice to the vector, increasing its
  length by the length of that slice. ``T`` is the type of the original vector
  or a type that can be implicitly cast to it. The following example tracks the
  elements inside ``vec`` through various appends. Note that the *element*
  size (``real[2]``) is fixed by the declaration and every appended element is
  padded or rejected against it, while the *number* of elements changes freely.

   ::

        const x = 1..10;
        var vector<real[2]> vec;       // []

        // scalar to array promotion
        vec.append(1);                 // [[1.0, 1.0]]

        // array padding
        vec.append(3..3);              // [[1.0, 1.0], [3.0, 0.0]]

        // slices
        vec.append(x[5..7]);           // [[1.0, 1.0], [3.0, 0.0], [5.0, 6.0]]

        vec.len() -> std_output;       // prints 3
        vec[vec.len()] -> std_output;  // prints [5 6]

