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
include src/CMakeFiles/preprocess.dir/depend.make

# Include the progress variables for this target.
include src/CMakeFiles/preprocess.dir/progress.make

# Include the compile flags for this target's objects.
include src/CMakeFiles/preprocess.dir/flags.make

src/CMakeFiles/preprocess.dir/preprocess.cpp.o: src/CMakeFiles/preprocess.dir/flags.make
src/CMakeFiles/preprocess.dir/preprocess.cpp.o: ../src/preprocess.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/jie/Desktop/vector_project/launch_computation_and_evaluation/tools/hpca-master/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object src/CMakeFiles/preprocess.dir/preprocess.cpp.o"
	cd /home/jie/Desktop/vector_project/launch_computation_and_evaluation/tools/hpca-master/build/src && g++   $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/preprocess.dir/preprocess.cpp.o -c /home/jie/Desktop/vector_project/launch_computation_and_evaluation/tools/hpca-master/src/preprocess.cpp

src/CMakeFiles/preprocess.dir/preprocess.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/preprocess.dir/preprocess.cpp.i"
	cd /home/jie/Desktop/vector_project/launch_computation_and_evaluation/tools/hpca-master/build/src && g++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/jie/Desktop/vector_project/launch_computation_and_evaluation/tools/hpca-master/src/preprocess.cpp > CMakeFiles/preprocess.dir/preprocess.cpp.i

src/CMakeFiles/preprocess.dir/preprocess.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/preprocess.dir/preprocess.cpp.s"
	cd /home/jie/Desktop/vector_project/launch_computation_and_evaluation/tools/hpca-master/build/src && g++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/jie/Desktop/vector_project/launch_computation_and_evaluation/tools/hpca-master/src/preprocess.cpp -o CMakeFiles/preprocess.dir/preprocess.cpp.s

src/CMakeFiles/preprocess.dir/preprocess.cpp.o.requires:

.PHONY : src/CMakeFiles/preprocess.dir/preprocess.cpp.o.requires

src/CMakeFiles/preprocess.dir/preprocess.cpp.o.provides: src/CMakeFiles/preprocess.dir/preprocess.cpp.o.requires
	$(MAKE) -f src/CMakeFiles/preprocess.dir/build.make src/CMakeFiles/preprocess.dir/preprocess.cpp.o.provides.build
.PHONY : src/CMakeFiles/preprocess.dir/preprocess.cpp.o.provides

src/CMakeFiles/preprocess.dir/preprocess.cpp.o.provides.build: src/CMakeFiles/preprocess.dir/preprocess.cpp.o


# Object files for target preprocess
preprocess_OBJECTS = \
"CMakeFiles/preprocess.dir/preprocess.cpp.o"

# External object files for target preprocess
preprocess_EXTERNAL_OBJECTS =

../bin/preprocess: src/CMakeFiles/preprocess.dir/preprocess.cpp.o
../bin/preprocess: src/CMakeFiles/preprocess.dir/build.make
../bin/preprocess: src/util/libutil.a
../bin/preprocess: /usr/lib/x86_64-linux-gnu/libz.so
../bin/preprocess: src/CMakeFiles/preprocess.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/jie/Desktop/vector_project/launch_computation_and_evaluation/tools/hpca-master/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable ../../bin/preprocess"
	cd /home/jie/Desktop/vector_project/launch_computation_and_evaluation/tools/hpca-master/build/src && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/preprocess.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
src/CMakeFiles/preprocess.dir/build: ../bin/preprocess

.PHONY : src/CMakeFiles/preprocess.dir/build

src/CMakeFiles/preprocess.dir/requires: src/CMakeFiles/preprocess.dir/preprocess.cpp.o.requires

.PHONY : src/CMakeFiles/preprocess.dir/requires

src/CMakeFiles/preprocess.dir/clean:
	cd /home/jie/Desktop/vector_project/launch_computation_and_evaluation/tools/hpca-master/build/src && $(CMAKE_COMMAND) -P CMakeFiles/preprocess.dir/cmake_clean.cmake
.PHONY : src/CMakeFiles/preprocess.dir/clean

src/CMakeFiles/preprocess.dir/depend:
	cd /home/jie/Desktop/vector_project/launch_computation_and_evaluation/tools/hpca-master/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/jie/Desktop/vector_project/launch_computation_and_evaluation/tools/hpca-master /home/jie/Desktop/vector_project/launch_computation_and_evaluation/tools/hpca-master/src /home/jie/Desktop/vector_project/launch_computation_and_evaluation/tools/hpca-master/build /home/jie/Desktop/vector_project/launch_computation_and_evaluation/tools/hpca-master/build/src /home/jie/Desktop/vector_project/launch_computation_and_evaluation/tools/hpca-master/build/src/CMakeFiles/preprocess.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : src/CMakeFiles/preprocess.dir/depend

