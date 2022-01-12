#!/bin/bash

outputname=ID1_ID2

rm ./$outputname.zip -f

zip ./$outputname.zip main.py persistence.py

