Setting up CLion
================

CLion requires a little bit of setup.

#. Open up CLion. If you've been using CLion and it opens to a previous project,
   select ``Close project``. Now that you're at the welcome screen, select
   ``Open or Import`` on the right. Navigate to where your project is located
   and select the folder that contains it. Select ``OK`` to open the project.

#. CLion doesn’t make use of your command line environment, it has its
   own storage place. Therefore we need to add ``ANTLR_INS`` to CLion’s
   environment.

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

      .. code-block:: console

       $ echo $ANTLR_INS

   #. Select ``OK`` to save your changes to the environment variables, select
      ``OK`` again to close the

#. We want to build all targets, not just the generator target. To do this we
   must add a new build configuration. If you have an older version of CLion
   this may already be present as a target called ``Build All``.

   #. From the build configuration drop-down menu on the toolbar (which likely
      says ``generator | Debug``) select ``Edit configurations``.

   #. In the new pane, select the ``+`` to add a new configuration and select
      ``CMake application``.

   #. Change the ``Name`` field to ``all`` and the target field to ``All
      targets``.

   #. Click ``OK`` to save the new target.

   #. From the build configuration drop-down menu, select your new target called
      ``all``.

   #. The build configuration menu should now show ``all | Debug``.

#. CLion may not automatically pick up ANTLR’s generated sources as your
   project’s. We can fix this by telling CLion where the files are.
   Build once to have the ``gen`` directory appear in the project
   manager pane. Right click on the directory, near the bottom of the
   menu find ``Mark directory as``, within that menu select
   ``Project Sources and Headers``.
