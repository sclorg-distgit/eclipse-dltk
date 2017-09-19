#!/bin/bash
set -e

NAME="eclipse-dltk"
TAG=R5_7_1
RELENG_TAG=f27ee597511de946a568c9b2b855419af2b0b00c
CORE_TAG=c45fb3fb9aeb153633877a4470a43182a782e4ac
RUBY_TAG=0bd3f535a226a1706384468ddd461f6f15c48ac9
SHELL_TAG=1bf836c3cc806644a1ff495c3bb29a05bb223ec5
TCL_TAG=d9f00abd4deedd91c33cd7348458a5d509b5fb49

rm -fr $NAME-$TAG
mkdir $NAME-$TAG
pushd $NAME-$TAG

wget http://git.eclipse.org/c/dltk/org.eclipse.dltk.releng.git/snapshot/org.eclipse.dltk.releng-$RELENG_TAG.tar.xz
tar xfs org.eclipse.dltk.releng-$RELENG_TAG.tar.xz
rm org.eclipse.dltk.releng-$RELENG_TAG.tar.xz
mv org.eclipse.dltk.releng-$RELENG_TAG org.eclipse.dltk.releng

wget http://git.eclipse.org/c/dltk/org.eclipse.dltk.core.git/snapshot/org.eclipse.dltk.core-$CORE_TAG.tar.xz
tar xfs org.eclipse.dltk.core-$CORE_TAG.tar.xz
rm org.eclipse.dltk.core-$CORE_TAG.tar.xz
mv org.eclipse.dltk.core-$CORE_TAG org.eclipse.dltk.core

wget http://git.eclipse.org/c/dltk/org.eclipse.dltk.ruby.git/snapshot/org.eclipse.dltk.ruby-$RUBY_TAG.tar.xz
tar xfs org.eclipse.dltk.ruby-$RUBY_TAG.tar.xz
rm org.eclipse.dltk.ruby-$RUBY_TAG.tar.xz
mv org.eclipse.dltk.ruby-$RUBY_TAG org.eclipse.dltk.ruby

wget http://git.eclipse.org/c/dltk/org.eclipse.dltk.tcl.git/snapshot/org.eclipse.dltk.tcl-$TCL_TAG.tar.xz
tar xfs org.eclipse.dltk.tcl-$TCL_TAG.tar.xz
rm org.eclipse.dltk.tcl-$TCL_TAG.tar.xz
mv org.eclipse.dltk.tcl-$TCL_TAG org.eclipse.dltk.tcl

wget http://git.eclipse.org/c/dltk/org.eclipse.dltk.sh.git/snapshot/org.eclipse.dltk.sh-$SHELL_TAG.tar.xz
tar xfs org.eclipse.dltk.sh-$SHELL_TAG.tar.xz
rm org.eclipse.dltk.sh-$SHELL_TAG.tar.xz
mv org.eclipse.dltk.sh-$SHELL_TAG org.eclipse.dltk.sh

popd

#Remove any commited jars
find $NAME-$TAG -name *.jar -delete
find $NAME-$TAG -name *.class -delete

echo "Creating tarball '$NAME-$TAG.tar.xz'..."
tar -caf $NAME-$TAG.tar.xz $NAME-$TAG
