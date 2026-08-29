.. _sec:errors_impl:

Errors (Implementation)
=======================

The **normative error taxonomy** -- the set of error classes and the condition
under which each must be emitted -- lives in the specification part, at
:ref:`sec:errors`. This chapter covers only the *mechanics* of reporting those
errors; the per-class notes below are implementation reminders that defer to
that taxonomy.

Your implementation is required to report both :term:`compile-time <compile time>` and :term:`run-time <run time>` errors.
You must use the exceptions defined in ``include/CompileTimeExceptions.h`` and
the functions defined in ``runtime/include/run_time_errors.h``. Do not modify
these files, you can pass a string to a constructor/function to provide more
details about a particular error. You must pass the corresponding line number to
the exceptions for compile-time errors but not run-time errors. Do not create
new errors. Your compiler is only expected to report the first error it
encounters.

Syntax Errors
-------------

ANTLR handles syntax errors automatically, but you are required to override the
behavior and throw the ``SyntaxError`` exception from
``include/CompileTimeExceptions.h``.

For example:

::

    /* main.cpp */

    class MyErrorListener : public antlr4::BaseErrorListener {
        void syntaxError(antlr4::Recognizer *recognizer, antlr4::Token * offendingSymbol,
                         size_t line, size_t charPositionInLine, const std::string &msg,
                         std::exception_ptr e) override {
            std::vector<std::string> rule_stack = ((antlr4::Parser*) recognizer)->getRuleInvocationStack();
            // The rule_stack may be used for determining what rule and context the error has occurred in.
            // You may want to print the stack along with the error message, or use the stack contents to 
            // make a more detailed error message.

            throw SyntaxError(line, msg); // Throw our exception with ANTLR's error message. You can customize this as appropriate.
        }
    };

    int main(int argc, char **argv) {

        ...

        gazprea::GazpreaParser parser(&tokens);

        parser.removeErrorListeners(); // Remove the default console error listener
        parser.addErrorListener(new MyErrorListener()); // Add our error listener

        ...
    }

For more information regarding the handling of syntax errors in ANTLR, refer to
chapter 9 of
`The Definitive ANTLR 4 Reference <https://pragprog.com/titles/tpantlr2/>`__.

Compile-time Errors
-------------------

:term:`Compile-time <compile time>` errors must be handled by throwing the exceptions defined in
``include/CompileTimeExceptions.h``. To throw an exception, use the ``throw``
keyword.

::

    throw MainError(1, "program does not have a main procedure");

The compiler must throw the following exceptions. Each corresponds to an error
class defined normatively in :ref:`sec:errors`; the notes here add
implementation-specific reminders (line numbers, tester leniency):

* ``SyntaxError``

    Raised during compilation if the parser encounters a syntactic error in the
    program.

* ``SymbolError``

    Raised during compilation if an undefined symbol is referenced or a defined
    symbol is re-defined in the same :term:`scope`.

* ``TypeError``

    Raised during compilation if an operation or statement is applied to or
    between expressions with invalid or incompatible types.

* ``AliasingError``

    Raised during compilation if the compiler detects that mutable memory
    locations may be aliased.

* ``AssignError``

    Raised during compilation if the compiler detects an assignment to a const
    value or a tuple unpacking assignment with the number of :term:`lvalues <lvalue>` different
    than the number of fields in the tuple :term:`rvalue`.

* ``MainError``

    Raised during compilation if the program does not have a procedure named
    ``main`` or when the signature of ``main`` is :term:`ill-formed`.

* ``ReturnError``

    Raised during compilation if the program detects a function or procedure
    with a return value that does not have a return statement reachable by all
    control flows. Control flow constructs may be assumed to always be undecidable,
    meaning they may branch in either direction. When the function or procedure is missing
    a reachable ``return`` statement, the line number of the function or
    procedure declaration should be printed.

    A ``return`` statement whose value's type does not match, and cannot be
    implicitly cast to, the owning function or procedure's return type is normalized as a
    ``TypeError`` (see the ``TypeError`` entry above and :ref:`sec:statements`),
    **not** a ``ReturnError``; the line number of the ``return`` statement
    should be reported, along with the name and (correct) type of the enclosing
    function or procedure. (The tester is lenient about the exact error name here -- it
    checks only for the substring "Error" and the line -- as noted at the end
    of this chapter.)

* ``GlobalError``

    Raised during compilation if the program detects a ``var`` global
    declaration, a global declaration without an initializing expression, a
    global declaration with an invalid initializing expression or any statement
    that does not belong in the global scope.

* ``StatementError``

    Raised during compilation if the program is syntactically valid but the
    compiler detects an invalid statement in some context. For example,
    ``continue`` or ``break`` outside of a loop body.

* ``CallError``

    Raised during compilation if the procedure call statement is used to call a
    function. Also raised if a procedure is called in an invalid context. For
    example, a procedure call in an output stream expression.

* ``DefinitionError``

    Raised during compilation if a procedure or function is declared but not
    defined.

* ``LiteralError``

    Raised during compilation if a literal value in the program does not fit
    into its corresponding data type.

* ``MathError``

    Raised for the integer math faults defined normatively in :ref:`ssec:integer`
    -- signed 32-bit overflow, division or ``%`` by ``0``, and exponentiation of
    base ``0`` with a non-positive exponent. ``real`` arithmetic never raises a
    ``MathError`` (it follows IEEE 754; see :ref:`ssec:real`). This error may be
    raised at compile time when the faulting expression is evaluated during
    constant folding; the conditions are identical to the :term:`runtime <run
    time>` ``MathError``.

* ``IndexError``

    May be raised during compilation if an expression used to index an array is an
    ``integer``, but is invalid for the array size.

* ``SizeError``

    May be raised during compilation if the compiler detects an operation or statement
    is applied to or between arrays with invalid or incompatible
    sizes. 

Here is an example invalid program and a corresponding compile-time error:

::

    1 procedure main() returns integer {
    2     integer x;
    3 }

::

    ReturnError on line 1: procedure "main" does not have a return statement reachable by all control flows

Run-time Errors
---------------

:term:`Run-time <run time>` errors must be handled by calling the functions defined in
``runtime/include/run_time_errors.h``.

::

    MathError("cannot divide by zero")

The runtime errors listed below are a subset of :term:`compile time` errors. Since it is not only impractical,
but undecidable to catch the following errors exclusively at compile time, Gazprea leaves the setting
at which they are raised up to the implementation. To put simply, you can raise runtime errors either
at compile time or at runtime and the tester will accommodate different implementations.

* ``SizeError``

    Raised at runtime if an operation or statement is applied to or between
    arrays with invalid or incompatible sizes. 

* ``IndexError``

    Raised at runtime if an expression used to index an array is an
    ``integer``, but is invalid for the array size.

* ``MathError``

    Raised at runtime for the integer math faults defined normatively in
    :ref:`ssec:integer` (signed 32-bit overflow, division or ``%`` by ``0``, and
    exponentiation of base ``0`` with a non-positive exponent). ``real``
    arithmetic never raises a ``MathError``; see :ref:`ssec:real`.

Here is an example :term:`ill-formed` program. If your compiler is smart, you may raise the later error, if you
prefer not to implement static analysis, the former error can be emitted at runtime.

::

    1 procedure main() returns integer {
    2     integer[3] x = [2, 4, 6];
    3     return x[4];
    4 }

::

    IndexError: This is a runtime error, invalid index "4" on array with size 3.

::
    
    IndexError on line 3: This is a compile time error, invalid index of "4" on array with size 3.
 

More Examples
-------------

::

   /* Indexes */
   var character[3] v = ['a', 'b', 'c']; // Indexing is harder than it looks!
   integer i = 10;
   v(3) = 'X'; // SyntaxError: a call expression cannot be an assignment target
   v[i] = '?'; // Runtime error
   v['a'] = '!'; // TypeError
   i[1] = 1; // TypeError

   /* Tuples */
   tuple (integer, integer) a = (9, 5);
   var integer b;
   var integer c;
   var integer d;
   b, c, d = a; // AssignError
   tuple(integer, integer, integer) z = a; // TypeError

``v(3) = 'X'`` is a ``SyntaxError`` because ``v(3)`` parses as a *call*
expression, and a call expression cannot appear on the left-hand side of an
assignment; the malformed assignment target is rejected at parse time, before
any type checking. (Indexing uses square brackets, ``v[3]``.) The ``b, c, d``
are declared ``var`` so that ``b, c, d = a;`` is purely the intended arity
mismatch (three lvalues, a two-field tuple) rather than also an assignment to
``const`` values -- both are ``AssignError``\ s, but the example is meant to
isolate the arity case.


How to Write an Error Test Case
-------------------------------

Your compiler test suite can include error test cases. An error test case can include
a :term:`compile-time <compile time>` or :term:`run-time <run time>` error. In either case, the expected output should include
exactly one line of text. In order to simplify marking, **only one error should be present in the test case**
and exactly one line of expected output should catch it. Below is an example:

::

  var integer x = 0;

  procedure main() returns integer {
    return 0;
  }

::

  GlobalError on line 1

Precisely defining the line number on which an error occurs can be difficult.
Should the ``AssignError`` below occur on line 3, 6 or in between? 

::

  procedure main() returns integer {
      const integer i = 5;
      i
      =
      5
      ;
  }

For this reason, test cases that deliberately make the line number ambiguous will be disqualified.
If an obvious line number is not apparent, refer to the reference solution on the 415
compiler explorer. For runtime errors, the line number is not required. Here is an
example of a run-time error test case and the corresponding expected output file:

::

  procedure main() returns integer {
    integer x = 0;
    5 / x -> std_output;
    return 0;
  }

::

  MathError

How to make the Tester Happy
------------------------------------------

For error test cases, the tester inspects the first line from ``stderr``.
Therefore, you must ensure that you do not pollute this stream with debug messages etc.

Additionally, the tester only knows to stop the toolchain prematurely if your program 
terminates with a non-zero exit code. Once you have caught an error make sure to return
a non-zero exit code.

Finally, the tester is lenient towards the type given to a particular error. Specifically
the tester simply confirms that the substring "Error" is present and for
:term:`compile time` errors that the correct line is provided.

This leniency is motivated by the fact that sometimes determining which type to call an error is
difficult. For example, it may be arguable that a ``ReturnError`` should be interpreted as a 
``TypeError`` and vice versa as previously mentioned.


