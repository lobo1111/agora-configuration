#!/bin/bash

GLASSFISH=/opt/glassfish/domains/domain1/autodeploy
PACKAGES=/opt/builder/src/target

sudo su -l glassfish --command="cp $PACKAGES/*.jar $GLASSFISH"%   