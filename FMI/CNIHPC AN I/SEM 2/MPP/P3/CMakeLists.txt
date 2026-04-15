cmake_minimum_required(VERSION 4.2)
project(P3)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(OpenMP REQUIRED)

set(CMAKE_CXX_FLAGS_RELEASE "-O2 -march=native")
add_executable(P3 main.cpp)

if(OpenMP_CXX_FOUND)
    target_link_libraries(P3 PUBLIC OpenMP::OpenMP_CXX)
endif()

add_executable(matrix_generator matrix_generator.cpp)

