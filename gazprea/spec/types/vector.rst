.. _ssec:vector:

Vectors
-------

Vectors are language supported objects that allow for dynamically sized arrays.
Once created, ``vectors`` in *Gazprea* behave exactly like arrays: they can be
intermixed with arrays in expressions; they can be used on the RHS of array
declarations and initializations; and they can be passed as array arguments to
subroutines and functions.

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


Unlike the array type, *Gazprea* vectors do not have an explicit size
specifier, often called *capacity* in other languages.

   ::

        vector<character> vec = ['a', 'b', 'c'];
        var vector<integer> ivec;
        vector<real[*]> ragged_right = [[1.0], [2.0, 2.0]];
        const vector<character> const_vec = vec;


As a language supported object, *Gazprea* provides several methods for ``vector``:

- push() - pushes a new element to the back of the vector

- len() - number of elements in the vector

- append - append another array slice to the vector
  
   ::

        var vector<tuple(bool, integer)> tvec;
        tvec.push((false, 0));
        tvec.append((true, 1));
        tvec[tvec.len()] -> std_output; // prints (true, 1)

Operations
~~~~~~~~~~~

Operations on vectors are identical syntactically and semantically to
operations on arrays. In particular, operand lengths must match for binary
expressions and dot product.

A vector or vector slice can be passed as a call argument that has been
declared as an array slice of the same size and type.

When indexing a vector of arrays, the first index selects the array element
within the vector, and the second index selects the element within the array:

 ::

        vector<real[*]> ragged_right = [[1.0], [2.1, 1.2]];
        length(ragged_right[1]) -> std_output; // prints 1
        ragged_right[2][2] -> std_output; // prints 1.2
