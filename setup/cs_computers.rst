CS Computers
============

This section details how to setup your environment to use the resources already
present on the CSC lab computers.

Using Prebuilt Resources
------------------------

Set up on the CSC machines is a lot simpler because all of the resources are
managed for you. Therefore, all you need to do is to add the provided
definitions to your ``~/.bashrc``.

::

     # C415 Predefinitions
     source "/cshome/cmput415/415-resources/415env.sh"

This should enable you to build manually using the command line. You should log
out and back in so that the changes can take effect.

.. _installing-clion-2:

Installing CLion
----------------

#. Go to the `download page
   <https://www.jetbrains.com/clion/download/#section=linux>`__ and download
   *CLion* for Linux.

#. Assuming you've downloaded the tarball to your ``~/Downloads`` folder, you
   can extract it to your home directory using the following command:

   .. code-block:: console

    $ sudo tar -xzf ~/Downloads/CLion-<version>.tar.gz -C ~

   If you are confident about your ability to setup your own install you can put
   it elsewhere but you will be on your own.

#. From now on, you can start *CLion* by using the following command:

   .. code-block:: console

    $ ~/CLion-<version>/bin/clion.sh

#. Perform the initial set up of CLion.

   #. Select ``Do not import settings`` and click ``OK``.

   #. Scroll to the bottom of the license agreement then hit ``Accept``.

   #. Choose if you want to share usage statistics.

   #. You should be presented with a prompt for your license. Select
      ``Activate``, ``JetBrains Account``, enter your UAlberta email address and
      JetBrains password. Click the ``Activate`` button.

   #. Pick your favorite UI. Then click ``Next: Toolchains``.

   #. Click ``Next: Default Plugins``.

   #. You might consider disabling all but the git plugin, and even
      then, using it is up to you. It can be useful to see the color coded files
      for differences at a glance or track changes in a file. You should
      consider disabling all of the web development plugins. Disabling other
      tools is up to you as well. Now select ``Next: Feature Plugins``

   #. Again, the choices here are yours. If you like vim, then maybe the
      vim plugin is up your alley. The markdown plugin can be useful as well.
      You do not need the TeamCity Integration, the Lua integration, nor the
      Swift integration. Select ``Start using CLion``
