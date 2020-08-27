Testing
=======

.. _testing_tool:

Testing Tool
------------

Inside the ``tests`` directory, a testing configuration file,
``GeneratorConfig.json``, is provided. You need to edit ``inDir`` with
the absolute path of ``…/tests/input``, ``outDir`` with the absolute
path of ``…/tests/output``, and finally ``testedExecutablePaths`` with
your ccid and the absolute path of ``…/bin/generator``.

Running the tester should now run your tests with your solution. Note
that the output files will not be cleaned up so it might be wise run
your tests in a directory that is not your repository. If you would
still like to run them in the same directory, just know that the output
files do not need to be tracked by git and can be safely deleted.

::

     tester <path_to_config>

For more information about the testing tool and how it works, see the
`Tester
README <https://github.com/cmput415/Tester/blob/master/README.md>`__.

Generating Test Cases
---------------------

A `Python script <https://github.com/cmput415/GeneratorFuzzer-Release>`__ ``fuzzer.py`` is 
available for automatic generation of random test cases.

More information is available in the README file included with the script,
but an example usage of the script is as follows:

::

     python fuzzer.py config.json test 10

The above command will generate two files ``test.in`` and ``test.out``, where
``test.in`` will contain 10 generators and ``test.out`` will contain 10 lines
containing the expected output for each of the respective generators. These files
can be placed in your ``tests`` directory for use with the :ref:`testing_tool`.
