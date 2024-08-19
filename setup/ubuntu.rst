Ubuntu
======

This section details how to setup your
Ubuntu
development environment.

Installing build-essential
--------------------------

On anything except a fresh install you've almost certainly installed this
package in the course of your regular development. In case you're working from
a fresh install, you'll need this first:

.. code-block:: console

 $ sudo apt-get update
 $ sudo apt-get install build-essential

Installing pkg-config
---------------------

pkg-config is a tool for querying installed libraries.

.. code-block:: console

 $ sudo apt-get update
 $ sudo apt-get install pkg-config

Installing libUUID
------------------

LibUUID is a library required for many applications so it's possible that you've
already installed this while installing something else. Best to try and install
it anyways:

.. code-block:: console

 $ sudo apt-get update
 $ sudo apt-get install uuid-dev

Installing OpenJDK JRE 17
-------------------------

The Java runtime environment (JRE) is required to run the ANTLR generator.
OpenJDK's JRE is easier to install than Oracle's, so we'll use that.

.. code-block:: console

 $ sudo apt-get update
 $ sudo apt-get install openjdk-17-jre

Installing Git
--------------

Git should be installed by default in Ubuntu. If you've removed it or it is
otherwise unavailable then you can install it using this command:

.. code-block:: console

 $ sudo apt-get update
 $ sudo apt-get install git

Installing CMake
----------------

Installing CMake from the package manager is easy too:

.. code-block:: console

 $ sudo apt-get update
 $ sudo apt-get install cmake

ANTLR 4 C++ Runtime
-------------------

This section details how to install the ANTLR 4 C++ runtime on Ubuntu
assuming your default shell is bash. If you've changed your shell from
bash it's assumed that you are familiar enough with your environment that
you can modify these steps appropriately.

#. To make things easy, we are going to do everything inside a new directory in
   your home directory.

   .. code-block:: console

    $ mkdir $HOME/antlr

   We'll refer to this directory (``$HOME/antlr``) as ``ANTLR_PARENT``.

#. Next we need to clone the runtime source from GitHub:

   .. code-block:: console

    $ cd <ANTLR_PARENT>
    $ git clone https://github.com/antlr/antlr4.git

   This should create a new folder called ``antlr4`` in ``ANTLR_PARENT``. We'll
   refer to this new directory (``<ANTLR_PARENT>/antlr4``) as ``SRC_DIR``.

#. We will be using ANTLR 4.13.0 so we need to change to the git tag for version
   4.13.0.

   .. code-block:: console

    $ cd <SRC_DIR>
    $ git checkout 4.13.0

   This will give you a warning about being in a “detached head state”. Since we
   won't be changing anything in ANTLR there is no need to create a branch. No
   extra work is needed here.

#. Now we need a place to build the runtime. CMake suggests making your build
   directory inside your source directory.

   .. code-block:: console

    $ cd <SRC_DIR>
    $ mkdir antlr4-build

   We'll refer to this new directory (``<SRC_DIR>/antlr4-build``) as
   ``BUILD_DIR``.

#. We need to have an install directory prepared before building since it's
   referenced in the build step. This directory will have the headers and
   compiled ANTLR libraries put into it. To make the actual directory:

   .. code-block:: console

    $ cd <ANTLR_PARENT>
    $ mkdir antlr4-install

   We'll refer to this new directory (``<ANTLR_PARENT>/antlr4-install``) as
   ``INSTALL_DIR``.

   Before continuing, if you're following this guide exactly, confirm your
   directory structure looks like this:

   .. code-block::

    $HOME
    +-- antlr/
        +-- antlr4/
        |   +-- antlr4-build/
        +-- antlr4-install/

#. Finally, we're ready to start the actual build process. Let's begin by doing
   the generate and configure CMake step for the runtime. We need to do this
   while inside the build directory. As well, we need to tell it that we want a
   release build and to install it to a certain directory.

   .. code-block:: console

    $ cd <BUILD_DIR>
    $ cmake <SRC_DIR>/runtime/Cpp/ \
        -DCMAKE_BUILD_TYPE=RELEASE \
        -DCMAKE_INSTALL_PREFIX="<INSTALL_DIR>"

   You will be presented with some CMake warnings but they're safe to ignore.

#. We can finally run ``make`` to build the library and install it. You can make
   the process significantly faster by running with multiple threads using the
   ``-j`` option and specifying a thread count. Using the option without a count
   will use unlimited threads. Be careful when using unlimited threads, the
   build has failed in the past due to limited resources. This isn't a big issue
   for the build because you can always just try again with a limited number of
   threads but your computer may appear to hang due to being over capacity.

   .. code-block:: console

    $ make install -j<number of threads>

#. Now we can add the install to your bash environment.
   Pick your favorite text editor, open ``~/.bashrc``,
   and add the following lines to the end, substituting appropriately:

   .. code-block:: shell

    # C415 ANTLR install
    export ANTLR_INS="<INSTALL_DIR>"

   **Make sure there is no trailing forward slash (/).** Close and reopen your terminal for
   things to take effect.

Installing CLion
----------------

#. Go to the `download page
   <https://www.jetbrains.com/clion/download/#section=linux>`__ and download
   *CLion* for Linux.

#. Assuming you've downloaded the tarball to your ``~/Downloads`` folder, you
   can extract it to
   ``/opt/``
   using the following command:

   .. code-block:: console

    $ sudo tar -xzf ~/Downloads/clion-<version>.tar.gz -C /opt/

   If you are confident about your ability to setup your own install you can put
   it elsewhere but you will be on your own.

#. From now on, you can start *CLion* by using the following command:

   .. code-block:: console

    $ /opt/clion-<version>/bin/clion.sh

#. Perform the initial set up of CLion.

   #. Select ``Do not import settings`` and click ``OK``.

   #. Scroll to the bottom of the license agreement then hit ``Accept``.

   #. Choose if you want to share usage statistics.

   #. You should be presented with a prompt for your license. Select
      ``Activate CLion``, ``JB Account``, click
      ``Log In to JetBrains Account...`` and enter your UAlberta email address
      and JetBrains account password. Click the ``Activate`` button.

   #. Pick your favorite UI. Then click ``Next: Toolchains``.

   #. CLion bundles a version of CMake with it. If you'd prefer to use the one
      we've just installed change ``Bundled`` to
      ``/usr/bin/cmake``.
      The
      info text beneath should update with a checkmark and the version of your
      installed cmake. Click ``Next: Default Plugins``.

   #. You might consider disabling all but the git plugin, and even then, using
      it is up to you. It can be useful to see the color coded files for
      differences at a glance or track changes in a file. You should consider
      disabling all of the web development plugins. Disabling other tools is up
      to you as well. Now select ``Next: Feature Plugins``

   #. Again, the choices here are yours. If you like vim, then maybe the vim
      plugin is up your alley. The markdown plugin can be useful as well. You do
      not need the TeamCity Integration, the Lua integration, nor the Swift
      integration. Select ``Start using CLion``

Installing the ANTLR Plugin for CLion
-------------------------------------

ANTLR has a CLion integration that gives syntax highlighting as well as tools
for visualising the parse tree for a grammar rule and an input.

#. Launch CLion by going to the application launcher
   (tap the super/Windows button)
   and typing ``clion``. This should launch CLion.

#. Open the settings window ``CLion`` :math:`\rightarrow` ``Preferences...``

#. Select ``Plugins`` from the menu on the left.

#. Click ``Browse Repositories...`` below the plugin list.

#. In the new window, type ``antlr`` into the search bar at the top.

#. From the list select ``ANTLR v4 grammar plugin``.

#. Click ``Install`` in the right pane and accept the notice.

#. After the install bar ends click the ``Restart CLion`` button that should
   have replaced the ``Install`` button.

Installing ANTLR Generator
--------------------------

If you'd like to manually generate a listener or visitor you need to have the
ANTLR generator. Follow these steps into install it:

#. Make the destination directory. I would suggest putting this in
   ``<INSTALL_DIR>/bin`` since the assignments will already automatically
   download a copy there and duplicating this seems wasteful. If you want to put
   it elsewhere though, you can.

   .. code-block:: console

    $ mkdir <INSTALL_DIR>/bin

   We'll refer to this new directory (e.g. ``<INSTALL_DIR>/bin``) as
   ``ANTLR_BIN``.

#. Next, download the tool.

   .. code-block:: console

    $ curl https://www.antlr.org/download/antlr-4.13.0-complete.jar \
        -o <ANTLR_BIN>/antlr-4.13.0-complete.jar

#. Now we can make it easy to use. Add the following lines to your
   ``~/.bashrc``:

   .. code-block:: shell

    # C415 ANTLR generator.
    export ANTLR_JAR="<ANTLR_BIN>/antlr-4.13.0-complete.jar"
    export CLASSPATH="$ANTLR_JAR:$CLASSPATH"
    alias antlr4="java -Xmx500M org.antlr.v4.Tool"
    alias grun='java org.antlr.v4.gui.TestRig'

#. Close and reopen your terminal for things to take effect. Now these commands
   should produce useful help outputs:

   .. code-block:: console

    $ antlr4
    $ grun

Installing MLIR
---------------

In the VCalc assignment and your final project you will be working with MLIR
and LLVM. Due to the complex nature (and size) of MLIR we did not want to include
it as a subproject. In fact, you may even want to defer the installation
until you're about to start your assignment. Here are the steps to get MLIR up and running.

#. Checkout LLVM to your machine

   .. code-block:: console

    $ git clone --depth 1 --branch llvmorg-18.1.8 https://github.com/llvm/llvm-project.git llvm-project-18.1.8
    $ cd llvm-project
    $ mkdir build && cd build
    $ export MLIR_INS=$(pwd)     # remember this to be <MLIR_INS>

#. Build MLIR (more details are available `here <https://mlir.llvm.org/getting_started>`__)

   .. code-block:: console

    $ cd $MLIR_INS
    $ cmake -G Ninja ../llvm \
        -DLLVM_ENABLE_PROJECTS=mlir \
        -DLLVM_BUILD_EXAMPLES=ON \
        -DLLVM_TARGETS_TO_BUILD="Native" \
        -DCMAKE_BUILD_TYPE=Release \
        -DLLVM_ENABLE_ASSERTIONS=ON
    $ ninja -j<number of threads>

#. Add these configuration lines to your ``~/.bashrc`` file so that you can use
   the MLIR tools and so that ``cmake`` will find your build.

   .. code-block:: shell

    export MLIR_INS="<MLIR_INS>" # look back to step 1 for MLIR_INS
    export MLIR_DIR="$MLIR_INS/lib/cmake/mlir/" # Don't change me.
    export PATH="$MLIR_INS/bin:$PATH" # Don't change me

Installing the Tester
---------------------

This is the tool you'll be using for testing your solutions locally. You'll be
building it yourself so that any changes later are easily obtainable.

If you encounter issues, please log them on the `GitHub issue tracker
<https://github.com/cmput415/Tester/issues>`__ or, if you want to, submit a pull
request and we'll review it!

#. We'll build the tool in your home directory.

   .. code-block:: console

    $ cd $HOME
    $ git clone https://github.com/cmput415/Tester.git

#. Next we'll make the build directory.

   .. code-block:: console

    $ cd Tester
    $ mkdir build

#. Now, the configure and generate step.

   .. code-block:: console

    $ cd build
    $ cmake ..

#. Finally, build the project.

   .. code-block:: console

    $ make

#. We could refer directly to the executable every time, but it's probably
   easier to just have it on our path. Add these lines to the end of your
   ``~/.bashrc``.

   .. code-block:: shell

    # C415 testing utility.
    export PATH="$HOME/Tester/bin/:$PATH"

#. Close and reopen your terminal to have changes take effect. Test the command
   to make sure it works.

   .. code-block:: console

    $ tester --help

For more info about organising your tests and creating a configuration (though
templates will be provided with your assignments) you can check `the Tester
README <https://github.com/cmput415/Tester/blob/master/README.md>`__.

Testing Your Environment
------------------------

Clone and build the first base repository from github classroom. If it builds, then ``antlr`` in particular has been
installed correctly. You will get an opportunity to test your MLIR installation when starting ``VCalc``.
