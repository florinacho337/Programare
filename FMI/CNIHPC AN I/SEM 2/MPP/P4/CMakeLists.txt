cmake_minimum_required(VERSION 4.2)
project(P4 CXX)

set(CMAKE_CXX_STANDARD 20)
find_package(MPI REQUIRED)

add_executable(P4 main.cpp)

target_link_libraries(P4 PRIVATE MPI::MPI_CXX)
add_executable(matrix_generator matrix_generator.cpp)
