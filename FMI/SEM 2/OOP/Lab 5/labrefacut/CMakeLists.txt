cmake_minimum_required(VERSION 3.24)
project(labrefacut C)

set(CMAKE_C_STANDARD 23)

add_executable(labrefacut main.c domain.c MyList.c service.c teste.c ui.c domain.h MyList.h ui.h teste.h service.h)
