Using Inja
----------

Inja is the string templating library you’ll be using in this
assignment. You’ll only need the most basic string replacement
functionality, even though it can `be much more
advanced <https://github.com/pantor/inja#tutorial>`__.

String templating looks like this:

::

     #include "nlohmann/json.hpp"
     #include "inja.hpp"

     #include <string>
     #include <iostream>

     using JSON = nlohmann::json;

     int main() {
       std::string name;
       int age;
       std::cout << "What's your name?\n";
       std::cin >> name;
       std::cout << "How old are you?\n";
       std::cin >> age;

       JSON data;
       data["name"] = name;
       data["age"] = age;

       std::string strTemplate =
         "Hi, {{ name }}!\n"
         "You are {{ age }} years old!\n";

       std::cout << inja::render(strTemplate, data);

       return 0;
     }

Let’s deconstruct the example. First we have the includes that give us
access to the ``json`` class that *inja* uses to store data as well as
the inja tools.

::

   #include "nlohmann/json.hpp"
   #include "inja.hpp"

Next we have a statement that’s purely for convenience purposes. It
aliases the ``json`` class to ``JSON``. If we didn’t use this we could
refer to the ``json`` class using the fully qualified name
``nlohmann::json``.

::

     using JSON = nlohmann::json;

Now we create our data object and fill it. If you have keys ``key1`` and
``key2`` that map to values ``value1`` and ``value2`` respectively, the
general syntax is:

::

       JSON data;
       data["key1"] = value1;
       data["key2"] = value2;
       ...

Almost done. You need to define your format string using the inja
syntax. To have the value replace the key in the string you need to
surround the key double braces like so: ``{{ keyname }}``.

::

     std::string strTemplate = "{{ key1 }} {{ key2 }}";

Finally, you need to ``render`` the data into the template:

::

     std::string result = inja::render(strTemplate, data);

