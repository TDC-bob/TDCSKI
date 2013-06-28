#!/bin/sh
find ./ -iname "*.pyc" -exec rm "{}" \;
nosetests3 -v
