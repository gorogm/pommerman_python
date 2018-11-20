import numpy as np
import ctypes
import time
import sys

if sys.platform == "win32":
    c = ctypes.cdll.LoadLibrary("C:/work/pommermanmunchen/build/Release/munchen.dll")
else:
    c = ctypes.cdll.LoadLibrary("/opt/work/pommerman_cpp/cmake-build-debug/libmunchen.so")

decision = c.c_tests()


