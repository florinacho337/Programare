cmake_minimum_required(VERSION 4.1)
project(P1)

set(CMAKE_CXX_STANDARD 20)

set(CMAKE_CXX_FLAGS_RELEASE "-O2 -march=native")
add_executable(P1 main.cpp)

add_executable(matrix_generator matrix_generator.cpp)
