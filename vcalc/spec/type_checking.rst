Type Checking and ASTs
----------------------

With the addition of another type that can be mixed in, type checking
becomes a necessity in *Vcalc*. This means ensuring that vectors and
scalars are where they belong. Most expressions allow the interchange of
vectors and scalars, but there’s a few cases where it is necessary to
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
   can be implicitly upcast integers).

-  Filters: the predicate must be a boolean (remember that integers can
   be implicitly downcast to booleans).

A good way to handle this now and plan ahead for *gazprea* is to start
building an abstract syntax tree (AST) from your parse tree as well as a
class that knows how to traverse it.

An AST will allow you to attach information in ways that make sense to
you. It allows you to strip away unecessary tokens from the parse tree
as well as allowing you to convert the parse tree into a new form that
also makes sense to you. This could mean normalising parts of the tree
to reduce code generation efforts, attaching information through fields
or entirely new nodes, and more.

You can find more advice in the AST Tips and Tricks section.

