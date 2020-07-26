import ctypes
import sys

if sys.platform == "win32":
    c = ctypes.cdll.LoadLibrary("C:/work/pommermanmunchen/build/Release/libpommerman.dll")
else:
    c = ctypes.cdll.LoadLibrary("/opt/work/pommerman_cpp/cmake-build-debug/libpommerman.so")

print("loaded shared lib")
decision = c.c_tests()


