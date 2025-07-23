Vectors
-------

Vectors are language supported objects that allow for dynamically sized arrays.
Once created, Vectors in *Gazprea* behave exactly like arrays: they can be
intermixed with arrays in expressions; they can be use on the RHS of array
declarations and initializations; and they can be passed as array arguments to
subroutines and functions.

.. _sssec:vec_decl:

Declaration
~~~~~~~~~~~

Vectors are declared and (optionally) initialized as follows.
(Note that we have replaced ``<>`` with ``|`` in the notation below since
the literals ``<`` and ``>`` are used in the declaration)

   ::

            Vector<|type|> |identifier|;
            Vector<|type|> |identifier| = |type-expr|;
            Vector<|type|> |identifier| = |type-array|;


Unlike the array type, *Gazprea* Vectors do not have an explicit size
specifier, often called *capacity* in other languages.

   ::

        Vector<character> vec = ['a', 'b', 'c'];
        var Vector<integer> ivec;
        Vector<real[*]> ragged_right = [[1.0], [2.0, 2.0]];
        const Vector<character> const_vec = vec;


As a language supported object, *Gazprea* provides several methods for ``Vector``:

- push() - pushes a new element to the back of the Vector

- len() - number of elements in the Vector

- append - append another array slice to the Vector
  
   ::

        var Vector<tuple(bool, integer)> tvec;
        tvec.push((false, 0));
        tvec.append((true, 1));
        tvec[tvec.len()] -> std_output; // prints (true, 1)

Operations
~~~~~~~~~~~

Operations on Vectors are identical syntactically and semantically to
operations on arrays. In particular, operand lengths must match for binary
expressions and dot product.

A Vector or Vector slice can be passed as a call argument that has been
declared as an array slice of the same size and type.

When indexing a Vector of arrays, the first index selects the array element
within the Vector, and the second index selects the element within the array:

 ::

        Vector<real[*]> ragged_right = [[1.0], [2.1, 1.2]];
        length(ragged_right[1]) -> std_output; // prints 1
        ragged_right[2][2] -> std_output; // prints 1.2
