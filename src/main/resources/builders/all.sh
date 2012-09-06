#!/bin/bash
sudo /etc/init.d/glassfish stop
SRC=/opt/builder/scripts
$SRC/download.sh
$SRC/build.sh
$SRC/update-db.sh
$SRC/update-scripts.sh
$SRC/deploy.sh
sudo /etc/init.d/glassfish start
