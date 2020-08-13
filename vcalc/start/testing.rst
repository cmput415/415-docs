Testing
=======

.. _testing_tool:

Testing Tool
------------

Inside the ``tests`` directory, a testing configuration file,
``VCalcConfig.json``, is provided. You need to edit
``inDir`` with the absolute path of ``…/tests/input``, ``outDir`` with
the absolute path of ``…/tests/output``, ``testedExecutablePaths`` with 
your ccid and the absolute path of ``…/bin/vcalc``, and finally ``runtimes``
with your ccid and the absolute path of ``…/bin/libvcalcrt.so``

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

.. todo:: WIP
