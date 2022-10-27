cmake_minimum_required(VERSION 3.4...3.18)
project(cmake_example)

####
#### DEPENDENCIES
####

find_package (Dependencies QUIET)

if (NOT ${Dependencies_FOUND})
    if (NOT EXISTS ${CMAKE_CURRENT_BINARY_DIR}/DependenciesConfig.cmake)
        file(DOWNLOAD https://raw.githubusercontent.com/germanespinosa/dependencies/main/DependenciesConfig.cmake ${CMAKE_CURRENT_BINARY_DIR}/DependenciesConfig.cmake)
    endif()
    set(Dependencies_DIR "${CMAKE_CURRENT_BINARY_DIR}")
    find_package (Dependencies REQUIRED)
endif()

####
#### END DEPENDENCIES
####

install_git_dependency( Json-cpp
        https://github.com/germanespinosa/json-cpp
        INCLUDE_DIRECTORIES include )

install_git_dependency( Pybind11
        https://github.com/pybind/pybind11
        ADD_SUBDIRECTORY
        INCLUDE_DIRECTORIES
        include )

include_directories(include)

set (json_cpp_files_python
        ${Json-cpp_FOLDER}/src/json_base.cpp
        ${Json-cpp_FOLDER}/src/json_base64.cpp
        ${Json-cpp_FOLDER}/src/json_buffer.cpp
        ${Json-cpp_FOLDER}/src/json_util.cpp
        src/json_descriptor.cpp
        src/json_python.cpp
        )

pybind11_add_module(cmake_example ${json_cpp_files_python})

# EXAMPLE_VERSION_INFO is defined by setup.py and passed into the C++ code as a
# define (VERSION_INFO) here.
target_compile_definitions(cmake_example
                           PRIVATE VERSION_INFO=${EXAMPLE_VERSION_INFO})

#    add_catch_test( python_module_tests
#            TEST_FILES
#            python/json-cpp2/src/json_python_tests.cpp
#            SOURCE_FILES ${json_cpp_module_files}
#            INCLUDE_DIRECTORIES include)
