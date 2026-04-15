cmake_minimum_required(VERSION 4.2)
project(P2)

set(CMAKE_CXX_STANDARD 20)

set(CMAKE_CXX_FLAGS_RELEASE "-O2 -march=native")
add_executable(P2 main.cpp)

add_executable(matrix_generator matrix_generator.cpp)
