#!/usr/bin/env python3
import sys
import os

currentDir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(currentDir)

from jdReplace.jdReplace import main
main()

