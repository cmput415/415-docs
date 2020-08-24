#! /bin/bash
BIN=$HOME/fbin
README=$BIN/README
PROFILE=$HOME/f.bash_profile

mkdir $BIN
ln -s /usr/bin/clang-3.6 $BIN/clang
ln -s /usr/bin/lli-3.6 $BIN/lli
ln -s /usr/lib/jvm/java-8-oracle/bin/java $BIN/java
ln -s /usr/lib/jvm/java-8-oracle/bin/javac $BIN/javac

echo "This directory was create by the setup scrip for the CMPUT 415" >> $README
echo "class. It contains links to programs used throughout the class" >> $README
echo "This directory can be deleted when the class is over" >> $README

echo "# These exports are for the antlr v4 environment and are used" >> $PROFILE
echo "# to setup the Antlr develoment environment" >> $PROFILE
echo "export JAVA_HOME=/usr/lib/jvm/java-8-oracle" >> $PROFILE
echo "export JRE_HOME=$JAVA_HOME/jre" >> $PROFILE
echo "export ANTLR4=/usr/local/lib/antlr-4.5.3-complete.jar" >> $PROFILE
echo "export CLASSPATH=\$ANTLR:\$CLASSPATH" >> $PROFILE
echo "export PATH=$BIN:\$PATH" >> $PROFILE
source $PROFILE
