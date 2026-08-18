Type Checking
-------------

Because there are multiple types (``int`` and ``vector``), type checking
becomes a necessity in *Vcalc*. This means ensuring that vectors and
scalars are where they belong. Most expressions allow the interchange of
vectors and scalars, but there are a few cases where it is necessary to
have one or the other.

Note that these rules are already in their respective sections, this
list just serves to bring further attention to where type checking is
important.

-  Ranges: lower and upper bounds must be integers.

-  Conditional Statements: must be booleans (remember that integers can
   be :term:`implicitly converted <implicit conversion>` to booleans).

-  Domains: in a :term:`domain expression` (generator, filter, index)
   the :term:`domain` must be a vector.

-  Generators: the expression must be an integer (remember that booleans
   can be implicitly converted to integers).

-  Filters: the predicate must be a boolean (remember that integers can
   be implicitly converted to booleans).

