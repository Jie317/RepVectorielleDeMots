# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.5

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/jie/Desktop/vector_project/launch_computation_and_evaluation/tools/hpca-master

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/jie/Desktop/vector_project/launch_computation_and_evaluation/tools/hpca-master/build

# Include any dependencies generated for this target.
include src/CMakeFiles/eval.dir/depend.make

# Include the progress variables for this target.
include src/CMakeFiles/eval.dir/progress.make

# Include the compile flags for this target's objects.
include src/CMakeFiles/eval.dir/flags.make

src/CMakeFiles/eval.dir/eval.cpp.o: src/CMakeFiles/eval.dir/flags.make
src/CMakeFiles/eval.dir/eval.cpp.o: ../src/eval.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/jie/Desktop/vector_project/launch_computation_and_evaluation/tools/hpca-master/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object src/CMakeFiles/eval.dir/eval.cpp.o"
	cd /home/jie/Desktop/vector_project/launch_computation_and_evaluation/tools/hpca-master/build/src && g++   $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/eval.dir/eval.cpp.o -c /home/jie/Desktop/vector_project/launch_computation_and_evaluation/tools/hpca-master/src/eval.cpp

src/CMakeFiles/eval.dir/eval.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/eval.dir/eval.cpp.i"
	cd /home/jie/Desktop/vector_project/launch_computation_and_evaluation/tools/hpca-master/build/src && g++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/jie/Desktop/vector_project/launch_computation_and_evaluation/tools/hpca-master/src/eval.cpp > CMakeFiles/eval.dir/eval.cpp.i

src/CMakeFiles/eval.dir/eval.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/eval.dir/eval.cpp.s"
	cd /home/jie/Desktop/vector_project/launch_computation_and_evaluation/tools/hpca-master/build/src && g++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/jie/Desktop/vector_project/launch_computation_and_evaluation/tools/hpca-master/src/eval.cpp -o CMakeFiles/eval.dir/eval.cpp.s

src/CMakeFiles/eval.dir/eval.cpp.o.requires:

.PHONY : src/CMakeFiles/eval.dir/eval.cpp.o.requires

src/CMakeFiles/eval.dir/eval.cpp.o.provides: src/CMakeFiles/eval.dir/eval.cpp.o.requires
	$(MAKE) -f src/CMakeFiles/eval.dir/build.make src/CMakeFiles/eval.dir/eval.cpp.o.provides.build
.PHONY : src/CMakeFiles/eval.dir/eval.cpp.o.provides

src/CMakeFiles/eval.dir/eval.cpp.o.provides.build: src/CMakeFiles/eval.dir/eval.cpp.o


# Object files for target eval
eval_OBJECTS = \
"CMakeFiles/eval.dir/eval.cpp.o"

# External object files for target eval
eval_EXTERNAL_OBJECTS =

../bin/eval: src/CMakeFiles/eval.dir/eval.cpp.o
../bin/eval: src/CMakeFiles/eval.dir/build.make
../bin/eval: src/util/libutil.a
../bin/eval: src/redsvd/libredsvd.a
../bin/eval: /usr/lib/x86_64-linux-gnu/libz.so
../bin/eval: /usr/lib/libblas.so.3gf
../bin/eval: /usr/lib/liblapack.so.3gf
../bin/eval: /usr/lib/libblas.so.3gf
../bin/eval: /usr/lib/liblapack.so.3gf
../bin/eval: src/CMakeFiles/eval.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/jie/Desktop/vector_project/launch_computation_and_evaluation/tools/hpca-master/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable ../../bin/eval"
	cd /home/jie/Desktop/vector_project/launch_computation_and_evaluation/tools/hpca-master/build/src && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/eval.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
src/CMakeFiles/eval.dir/build: ../bin/eval

.PHONY : src/CMakeFiles/eval.dir/build

src/CMakeFiles/eval.dir/requires: src/CMakeFiles/eval.dir/eval.cpp.o.requires

.PHONY : src/CMakeFiles/eval.dir/requires

src/CMakeFiles/eval.dir/clean:
	cd /home/jie/Desktop/vector_project/launch_computation_and_evaluation/tools/hpca-master/build/src && $(CMAKE_COMMAND) -P CMakeFiles/eval.dir/cmake_clean.cmake
.PHONY : src/CMakeFiles/eval.dir/clean

src/CMakeFiles/eval.dir/depend:
	cd /home/jie/Desktop/vector_project/launch_computation_and_evaluation/tools/hpca-master/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/jie/Desktop/vector_project/launch_computation_and_evaluation/tools/hpca-master /home/jie/Desktop/vector_project/launch_computation_and_evaluation/tools/hpca-master/src /home/jie/Desktop/vector_project/launch_computation_and_evaluation/tools/hpca-master/build /home/jie/Desktop/vector_project/launch_computation_and_evaluation/tools/hpca-master/build/src /home/jie/Desktop/vector_project/launch_computation_and_evaluation/tools/hpca-master/build/src/CMakeFiles/eval.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : src/CMakeFiles/eval.dir/depend

