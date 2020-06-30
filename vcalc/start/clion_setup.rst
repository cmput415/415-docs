Setting up CLion
----------------

CLion requires a little bit of setup. Much of it is the same, but we
need to add LLVM now.

#. Open up CLion. From the welcome screen select
   ``Import Project from Sources`` or, if you’ve been using CLion and it
   opens to previous project, from the ``File`` menu select
   ``Import Project…``. Navigate to where your project is located an
   choose it. Choose ``Open Project`` *not*
   ``Overwrite CMakeLists.txt``. If you already have a project open, you
   can choose to use your current window or create another one.

#. CLion doesn’t make use of your command line environment, it has its
   own storage place. Therefore we need to add ``ANTLR_INS`` and
   ``LLVM_DIR`` to CLion’s environment.

   #. Open your settings. On Linux this is ``File`` :math:`\rightarrow`
      ``Settings…``, while on MacOS this is ``CLion``
      :math:`\rightarrow` ``Preferences…``.

   #. From the left menu, expand ``Build, Execution, Deployment``.

   #. Select ``CMake`` from the newly expanded options.

   #. In the right pane, select the ``…`` to the right of the empty text
      field to the right of ``Environment``.

   #. In the new pane, select the ``+`` symbol to add a new entry in the
      environment. On Linux this is in the top right of the pane, while
      on MacOS this is in the bottom left of the pane.

   #. In the new text field under ``Name`` enter ``ANTLR_INS``. In the
      field under ``Value`` enter the path to your ``antlr_install``
      directory. If you’ve forgotten it but your terminal is set up
      correctly, or if you’re using the lab machines, then you can enter
      the following command to print it:

      ::

                   echo $ANTLR_INS

   #. Select the ``+`` symbol to add another symbol to your environment.
      In the field under ``Name`` enter ``LLVM_DIR``. Since the value
      depends on how you have set up your environment (or how we have if
      you’re using the lab machines) you will need to enter this command
      in your terminal to find the value.

      ::

                   echo $LLVM_DIR

      Add this value in the ``Value`` field.

   #. Apply all of your changes while closing the settings.

#. Make sure you’re building the ``all`` target, not just the ``scalc``
   target. From the drop down menu in the top right of the IDE you can
   choose your build target. Change this to ``Build All``.

#. CLion may not automatically pick up ANTLR’s generated sources as your
   project’s. We can fix this by telling CLion where the files are.
   Build once to have the ``gen`` directory appear in the project
   manager pane. Right click on the directory, near the bottom of the
   menu find ``Mark directory as``, within that menu select
   ``Project Sources and Headers``.

