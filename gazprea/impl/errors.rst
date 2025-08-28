.. _sec:errors:

Errors
======

Your implementation is required to report both compile-time and run-time errors.
You must use the exceptions defined in ``include/CompileTimeExceptions.h`` and
the functions defined in ``runtime/include/run_time_errors.h``. Do not modify
these files, you can pass a string to a constructor/function to provide more
details about a particular error. You must pass the corresponding line number to
the exceptions for compile-time errors but not run-time errors. Do not create
new errors. Your compiler is only expected to report the first error it
encounters.

Syntax Errors
~~~~~~~~~~~~~

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

Compile-time errors must be handled by throwing the exceptions defined in
``include/CompileTimeExceptions.h``. To throw an exception, use the ``throw``
keyword.

::

    throw MainError(1, "program does not have a main procedure");

Here are the compile-time errors your compiler must throw: 

* ``SyntaxError``

    Raised during compilation if the parser encounters a syntactic error in the
    program.

* ``SymbolError``

    Raised during compilation if an undefined symbol is referenced or a defined
    symbol is re-defined in the same scope.

* ``TypeError``

    Raised during compilation if an operation or statement is applied to or
    betweeen expressions with invalid or incompatible types.

* ``AliasingError``

    Raised during compilation if the compiler detects that mutable memory
    locations may be aliased.

* ``AssignError``

    Raised during compilation if the compiler detects an assignment to a const
    value or a tuple unpacking assignment with the number of lvalues different
    than the number of fields in the tuple rvalue.

* ``MainError``

    Raised during compilation if the program does not have a procedure named
    ``main`` or when the signature of ``main`` is invalid.

* ``ReturnError``

    Raised during compilation if the program detects a function or procedure
    with a return value that does not have a return statement reachable by all
    control flows. Control flow constructs may be assumed to always be undecideable,
    meaning they may branch in either direction.

    If the subroutine has a ``return`` statement with a type that does not
    match the owning subroutine's type, the line number of the ``return``
    statement should be reported, along with the name and (correct) type of the
    enclosing routine.

    Note also that, strictly speaking, this is a type error, not a return error.
    If the procedure/function is missing a ``return`` statement, then the line
    number of the subroutine declaration should be printed instead.

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

    Raised during compile time expression evaluation when division by zero occurs.
    Conditions for raising are eqivalent to a runtime ``MathError``. 

* ``IndexError``

    Raised during compilation if an expression used to index an array is an
    ``integer``, but is invalid for the array size.

* ``SizeError``

    Raised during compilation if the compiler detects an operation or statement
    is applied to or between arrays with invalid or incompatible
    sizes. Read more about when a ``SizeError`` should be raised at run-time
    instead of compile-time in the :ref:`ssec:errors_sizeErrors` section.

* ``StrideError``

    Raised during compilation if the ``by`` operation is used with a stride value
    ``<=0``.

Here is an example invalid program and a corresponding compile-time error:

::

    1 procedure main() returns integer {
    2     integer x;
    3 }

::

    ReturnError on line 1: procedure "main" does not have a return statement reachable by all control flows

Run-time Errors
---------------

Run-time errors must be handled by calling the functions defined in
``runtime/include/run_time_errors.h``.

::

    MathError("cannot divide by zero")

Here are the run-time errors you need to report:

* ``SizeError``

    Raised at runtime if an operation or statement is applied to or between
    arrays with invalid or incompatible sizes. Read more about
    when a ``SizeError`` should be raised at compile-time instead of run-time in
    the :ref:`ssec:errors_sizeErrors` section.

* ``IndexError``

    Raised at runtime if an expression used to index an array is an
    ``integer``, but is invalid for the array size.

* ``MathError``

    Raised at runtime if either zero to the power of N, where N is <= 0, or a
    division by zero is evaluated.

* ``StrideError``

    Raised at runtime if the ``by`` operation is used with a stride value
    ``<=0``.

Here is an example invalid program and a corresponding run-time error:

::

    1 procedure main() returns integer {
    2     integer[3] x = [2, 4, 6];
    3     return integer[4];
    4 }

::

    IndexError: invalid index "4" on array with size 3

.. _ssec:errors_sizeErrors:


Ambiguous Errors
------------------------------------
Certain error types can be raised either at compile time or runtime depending on their context.
All of the runtime-errors listed above can be raised at compile time under simplified conditions,
for example, a compile time `SizeError` may be raised when adding two array literals of different size,
or may be rasied at runtime, for example when expression sizes can not be statically determined at compile
time. For such errors it is implementation defined whether the compiler is proactive in identifying
compile time errors, through tracking expression sizes and types, or defers the task to the runtime.


More Examples
-------------

::

   /* Indexes */
   character[3] v = ['a', 'b', 'c']; // Indexing is harder than it looks!
   integer i = 10;
   v(3) = 'X'; // SyntaxError
   v[i] = '?'; // Run-timeerror
   v['a'] = '!'; // TypeError
   i[1] = 1; // SymbolError

   /* Tuples */
   tuple (integerm integer) a = (9, 5);
   integer b;
   integer c;
   integer d;
   b, c, d = a; // AssignError
   tuple(integer, integer, integer) z = a; // TypeError


How to Write an Error Test Case
-------------------------------

Your compiler test suite can include error test cases. An error test case can include
a compile-time or run-time error. In either case, the expected output should include
exactly one line of text.

For error tests, **only one error should be present in the test case** and
exactly one line of expected output should catch it. The single line should include the error
type and the line number on which it occurs. Below is an example:

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

Test cases that deliberately make the line number ambiguous will be disqualified.
If an obvious line number is not apparent, refer to the reference solution on the 415
compiler explorer. For runtime errors, the line number is not required. Here is an
example of a run-time error test case and the corresponding expected output file:

::

  procedure main() returns integer {
    1..1 by 0 -> std_output;
    return 0;
  }

::

  StrideError

How to make the Tester Happy
------------------------------------------

For error test cases, the tester inspects the first line from ``stderr``.
Therefore, you must ensure that you do not pollute this stream with debug messages etc.

Additionally, the tester only knows to stop the toolchain prematurely if your program 
terminates with a non-zero exit code. Once you have caught an error make sure to return
a non-zero exit code.

Finally, the tester is lenient towards the type given to a particular errror. Specifically
the tester simply confirms that the substring "Error" is present and for compile
time errors that the correct line is provided.

This leniency is motivated by the fact that sometimes determining which type to call an error is
difficult. For example, it may be arguable that a ``ReturnError`` should be interpreted as a 
``TypeError`` and vice versa as previously mentioned.


