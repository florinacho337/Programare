cmake_minimum_required(VERSION 4.2)
project(P5 CXX)

set(CMAKE_CXX_STANDARD 20)
find_package(MPI REQUIRED)
find_package(OpenMP REQUIRED)

add_executable(P5 main.cpp)

target_link_libraries(P5 PRIVATE MPI::MPI_CXX OpenMP::OpenMP_CXX)
add_executable(matrix_generator matrix_generator.cpp)