AST Tips and Hints
==================

This section is likely to be constantly updated as new questions are
asked or useful things are found. You will be notified as appropriate.

-  At first glance, ASTs may not seem to provide much value. Much of
   your *VCalc* AST will be identical to your parse tree. There are,
   however, good reasons to make use of them now. A motivating example:

   ::

            print(a + b);

   What are ``a`` and ``b``? Integers? Vectors? One of each? How does
   your code generator know? Your AST can help you. You have a few
   options:

   #. Make your code generator figure it out.

   #. Attach type information to your AST at this node denoting each
      operands type during a type inference pass on your tree. Still
      need to check for extension.

   #. Do a type inference pass and replace the integer operand with an
      extension node so we only need to check the type of one operand to
      know the result type.

   #. Swap the operator node for a vector operator node and have the
      code generator assume that the non-vector version has integer
      operands while the vector one needs to check if there’s an integer
      to extend.

   #. Add type information to the above solution so we only need to
      check that.

   #. Don’t add type information and instead swap the operand node for
      an explict extension node and have both operator nodes assume the
      operands are of the right type.

   #. Anything else. It’s up to you.

   This is just one example of where you could possibly use an AST to
   make your life easier along the way.

-  You should create a tree traversal class in the same vein as ANTLR
   and its BaseVisitors. This way you can use the same mechanism for
   manipulating the tree, type checking, or final code generation.

-  An AST is not a “scope tree”. You can maintain a stack of tables that
   tell you what is currently in scope as you *traverse the tree* but
   scoping is not inherently part of the ast.

