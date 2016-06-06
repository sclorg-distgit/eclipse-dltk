#!/bin/bash
set -e

NAME="eclipse-dltk"
TAG=R5_4_0

rm -fr $NAME-$TAG
mkdir $NAME-$TAG
pushd $NAME-$TAG

wget http://git.eclipse.org/c/dltk/org.eclipse.dltk.releng.git/snapshot/org.eclipse.dltk.releng-$TAG.tar.xz
tar xfs org.eclipse.dltk.releng-$TAG.tar.xz
rm org.eclipse.dltk.releng-$TAG.tar.xz
mv org.eclipse.dltk.releng-$TAG org.eclipse.dltk.releng

wget http://git.eclipse.org/c/dltk/org.eclipse.dltk.core.git/snapshot/org.eclipse.dltk.core-$TAG.tar.xz
tar xfs org.eclipse.dltk.core-$TAG.tar.xz
rm org.eclipse.dltk.core-$TAG.tar.xz
mv org.eclipse.dltk.core-$TAG org.eclipse.dltk.core

wget http://git.eclipse.org/c/dltk/org.eclipse.dltk.ruby.git/snapshot/org.eclipse.dltk.ruby-$TAG.tar.xz
tar xfs org.eclipse.dltk.ruby-$TAG.tar.xz
rm org.eclipse.dltk.ruby-$TAG.tar.xz
mv org.eclipse.dltk.ruby-$TAG org.eclipse.dltk.ruby

wget http://git.eclipse.org/c/dltk/org.eclipse.dltk.tcl.git/snapshot/org.eclipse.dltk.tcl-$TAG.tar.xz
tar xfs org.eclipse.dltk.tcl-$TAG.tar.xz
rm org.eclipse.dltk.tcl-$TAG.tar.xz
mv org.eclipse.dltk.tcl-$TAG org.eclipse.dltk.tcl

wget http://git.eclipse.org/c/dltk/org.eclipse.dltk.sh.git/snapshot/org.eclipse.dltk.sh-$TAG.tar.xz
tar xfs org.eclipse.dltk.sh-$TAG.tar.xz
rm org.eclipse.dltk.sh-$TAG.tar.xz
mv org.eclipse.dltk.sh-$TAG org.eclipse.dltk.sh

popd

#Remove any commited jars
find $NAME-$TAG -name *.jar -delete
find $NAME-$TAG -name *.class -delete

echo "Creating tarball '$NAME-$TAG.tar.xz'..."
tar -caf $NAME-$TAG.tar.xz $NAME-$TAG
