#! /usr/bin/env python

from pylibpd import *
import time

print(libpd_init_audio(0,2,-44000))

patchid = libpd_open_patch("py.pd")


print patchid

