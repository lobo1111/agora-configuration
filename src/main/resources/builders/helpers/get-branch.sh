#!/bin/bash

git branch | grep \* | cut -d" " -f2
exit $?