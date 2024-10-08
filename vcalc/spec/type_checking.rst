Type Checking
-------------

With the addition of another type that can be mixed in, type checking
becomes a necessity in *Vcalc*. This means ensuring that vectors and
scalars are where they belong. Most expressions allow the interchange of
vectors and scalars, but there are a few cases where it is necessary to
have one or the other.

Note that these rules are already in their respective sections, this
list just serves to bring further attention to where type checking is
important.

-  Ranges: lower and upper bounds must be integers.

-  Conditional Statements: must be booleans (remember that integers can
   be implicitly downcast to booleans).

-  Domains: in a domain expression (generator, filter, index) the domain
   must be a vector.

-  Generators: the expression must be an integer (remember that booleans
   can be implicitly upcast to integers).

-  Filters: the predicate must be a boolean (remember that integers can
   be implicitly downcast to booleans).

