Errors
======

Your implementation is required to report both compile-time and runtime errors.

Your compiler must throw the exceptions defined in
``include/CompileTimeExceptions.h`` and ``runtime/src/RunTimeExceptions.h``.
Do not modify these files, you can pass a string to an exception to provide more
details about a particular error. You must pass the corresponding line number to
the exceptions for compile-time errors but not run-time errors. Do not create
new exceptions. Your compiler is only expected to report the first error it
encounters. Here is a list of the types of errors expected at compile-time and
run-time:

**Compile-time Errors**

* ``GazpreaSyntaxError``

    Raised during compilation if the parser encounters a syntactic error in the
    program.

* ``GazpreaSymbolError``
    
    Raised during compilation if an undefined symbol is referenced or a defined
    symbol is re-defined in the same scope.
    
* ``GazpreaTypeError``

    Raised during compilation if an operation or statement is applied to or
    betweeen expressions with invalid or incompatible types.

* ``GazpreaAliasingError``

    Raised during compilation if the compiler detects that mutable memory
    locations are aliased.

* ``GazpreaAssignError``

    Raised during compilation if the compiler detects an assignment to a const
    value or a tuple unpacking assignment with the number of lvalues different
    than the number of fields in the tuple rvalue.

* ``GazpreaMainError``

    Raised during compilation if the program does not have a procedure named
    ``main`` or when the signature of ``main`` is invalid.

* ``GazpreaReturnError``

    Raised during compilation if the program detects a function or procedure
    with a return value that does not have a return statement reachable by all
    control flows.

* ``GazpreaGlobalError``

    Raised during compilation if the program detects a ``var`` global
    declaration, a global declaration without an initializing expression, or a
    global declaration with an invalid initializing expression.

* ``GazpreaStatementError``

    Raised during compilation if the program is syntactically valid but the
    compiler detects an invalid statment in a some context. For example,
    ``continue`` or ``break`` outside of a loop body.

* ``GazpreaCallError``

    Raised during compilation if the procedure call statement is used to call a
    function.

* ``GazpreaDefinitionError``

    Raised during compilation if a procedure or function is declared but not
    defined.

* ``GazpreaSizeError``

    Raised during compilation if a 

Here is an example invalid program and a corresponding compile-time error:

::

    1 procedure main() returns integer {
    2     integer x;
    3 }

::

    GazpreaReturnError on line 1: procedure "main" does not have a return statement reachable by all control flows


**Run-time Errors**

* ``GazpreaSizeError``

    Raised at runtime if an operation or statement is applied to or between
    vectors and matrices with invalid or incompatible sizes.

* ``GazpreaIndexError``

    Raised at runtime if an expression used to index a vector or matrix is an
    ``integer``, but is invalid for the vector/matrix size.
    
* ``GazpreaDivisionError``
    
    Raised at runtime if a division by zero is detected.
    
* ``GazpreaStrideError``
    
    Raised at runtime if the ``by`` operation is used with a stride value of
    ``0``.

Here is an example invalid program and a corresponding run-time error:

::

    1 procedure main() returns integer {
    2     integer[3] x = [2, 4, 6];
    3     return integer[4];
    4 }

::
    
    GazpreaIndexError: invalid index "4" on vector with size 3

How to Write an Error Test Case
-------------------------------

Your compiler test-suite can include error test cases. An error test case can be
a compile-time error test case or a run-time error test case. In either case,
the last line of the corresponding expected output file should be the substring
of the error message preceding the colon.

Compile-time test cases should be exactly one line since the compilation failed.



Any test case whose 


Compile-time Errors
-------------------

Compile-time errors must be handled by throwing `C++ standard exceptions <http://www.cplusplus.com/doc/tutorial/exceptions/>`__.

You should create different exception classes for each of the different kinds of compile-time errors you report, such as a Type Error shown in the example below.

You must create all your exception classes in a single header file ``exceptions.h`` and extend ``std::exception``.

Example exception class:

::

    /* exceptions.h */

    #include <string>
    #include <sstream>

    class TypeError : public std::exception {
    private:
        std::string msg;
    public:
        TypeError(std::string lhs, std::string rhs, int line) {
            std::stringstream sstream;
            sstream << "Type error: Cannot convert between "
                    << lhs << " and " << rhs << " on line " << line << "\n";
            msg = sstream.str();
        }

        virtual const char* what() const throw() {
            return msg.c_str();
        }
    };

Whenever you encounter an error, you throw an appropriate exception.
To throw an exception, use the ``throw`` keyword. As an example for the exception defined above, we throw it as follows:

::

    throw TypeError("int", "char", 10);

Syntax Errors
~~~~~~~~~~~~~

Syntax errors are also compile-time errors. ANTLR handles syntax errors automatically, but you are required to override the behavior and throw your own exception from ``exceptions.h``.

Example:

::

    /* exceptions.h */

    #include <string>
    #include <sstream>

    class SyntaxError : public std::exception {
    private:
        std::string msg;
    public:
        SyntaxError(std::string msg) : msg(msg) {}

        virtual const char* what() const throw() {
            return msg.c_str();
        }
    };

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

            throw SyntaxError(msg); // Throw our exception with ANTLR's error message. You can customize this as appropriate.
        }
    };

    int main(int argc, char **argv) {

        ...

        gazprea::GazpreaParser parser(&tokens);

        parser.removeErrorListeners(); // Remove the default console error listener
        parser.addErrorListener(new MyErrorListener()); // Add our error listener

        ...
    }

For more information regarding the handling of syntax errors in ANTLR, refer to chapter 9 of `The Definitive ANTLR 4 Reference <https://pragprog.com/titles/tpantlr2/>`__.


Run-time Errors
---------------

Since the runtime library is written in C, you do not have access to C++ standard exceptions.

Instead, you are required to have a single header file ``errors.h`` containing all your functions which print error messages to ``stderr`` and exit.

Simply call any of the functions when you need to report an error.

Example:

::

    /* errors.h */

    #include <stdlib.h>

    void sizeMismatchError() {
        fprintf(stderr, "Size mismatch error: Can not operate between two vectors or matrices of differing size");
        exit(1);
    }
