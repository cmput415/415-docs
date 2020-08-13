Errors
======

Your implementation is required to report both compile-time and runtime errors.

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


Runtime Errors
--------------

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
