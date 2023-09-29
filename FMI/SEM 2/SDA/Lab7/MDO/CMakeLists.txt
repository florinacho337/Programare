cmake_minimum_required(VERSION 3.25)
project(MDO)

set(CMAKE_CXX_STANDARD 17)

add_executable(MDO main.cpp IteratorMDO.cpp MDO.cpp TestExtins.cpp TestScurt.cpp)
