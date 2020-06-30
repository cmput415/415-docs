Testing
=======

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

