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
include src/CMakeFiles/cooccurrence.dir/depend.make

# Include the progress variables for this target.
include src/CMakeFiles/cooccurrence.dir/progress.make

# Include the compile flags for this target's objects.
include src/CMakeFiles/cooccurrence.dir/flags.make

src/CMakeFiles/cooccurrence.dir/cooccurrence.cpp.o: src/CMakeFiles/cooccurrence.dir/flags.make
src/CMakeFiles/cooccurrence.dir/cooccurrence.cpp.o: ../src/cooccurrence.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/jie/Desktop/vector_project/launch_computation_and_evaluation/tools/hpca-master/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object src/CMakeFiles/cooccurrence.dir/cooccurrence.cpp.o"
	cd /home/jie/Desktop/vector_project/launch_computation_and_evaluation/tools/hpca-master/build/src && g++   $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/cooccurrence.dir/cooccurrence.cpp.o -c /home/jie/Desktop/vector_project/launch_computation_and_evaluation/tools/hpca-master/src/cooccurrence.cpp

src/CMakeFiles/cooccurrence.dir/cooccurrence.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/cooccurrence.dir/cooccurrence.cpp.i"
	cd /home/jie/Desktop/vector_project/launch_computation_and_evaluation/tools/hpca-master/build/src && g++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/jie/Desktop/vector_project/launch_computation_and_evaluation/tools/hpca-master/src/cooccurrence.cpp > CMakeFiles/cooccurrence.dir/cooccurrence.cpp.i

src/CMakeFiles/cooccurrence.dir/cooccurrence.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/cooccurrence.dir/cooccurrence.cpp.s"
	cd /home/jie/Desktop/vector_project/launch_computation_and_evaluation/tools/hpca-master/build/src && g++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/jie/Desktop/vector_project/launch_computation_and_evaluation/tools/hpca-master/src/cooccurrence.cpp -o CMakeFiles/cooccurrence.dir/cooccurrence.cpp.s

src/CMakeFiles/cooccurrence.dir/cooccurrence.cpp.o.requires:

.PHONY : src/CMakeFiles/cooccurrence.dir/cooccurrence.cpp.o.requires

src/CMakeFiles/cooccurrence.dir/cooccurrence.cpp.o.provides: src/CMakeFiles/cooccurrence.dir/cooccurrence.cpp.o.requires
	$(MAKE) -f src/CMakeFiles/cooccurrence.dir/build.make src/CMakeFiles/cooccurrence.dir/cooccurrence.cpp.o.provides.build
.PHONY : src/CMakeFiles/cooccurrence.dir/cooccurrence.cpp.o.provides

src/CMakeFiles/cooccurrence.dir/cooccurrence.cpp.o.provides.build: src/CMakeFiles/cooccurrence.dir/cooccurrence.cpp.o


# Object files for target cooccurrence
cooccurrence_OBJECTS = \
"CMakeFiles/cooccurrence.dir/cooccurrence.cpp.o"

# External object files for target cooccurrence
cooccurrence_EXTERNAL_OBJECTS =

../bin/cooccurrence: src/CMakeFiles/cooccurrence.dir/cooccurrence.cpp.o
../bin/cooccurrence: src/CMakeFiles/cooccurrence.dir/build.make
../bin/cooccurrence: src/util/libutil.a
../bin/cooccurrence: /usr/lib/x86_64-linux-gnu/libz.so
../bin/cooccurrence: src/CMakeFiles/cooccurrence.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/jie/Desktop/vector_project/launch_computation_and_evaluation/tools/hpca-master/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable ../../bin/cooccurrence"
	cd /home/jie/Desktop/vector_project/launch_computation_and_evaluation/tools/hpca-master/build/src && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/cooccurrence.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
src/CMakeFiles/cooccurrence.dir/build: ../bin/cooccurrence

.PHONY : src/CMakeFiles/cooccurrence.dir/build

src/CMakeFiles/cooccurrence.dir/requires: src/CMakeFiles/cooccurrence.dir/cooccurrence.cpp.o.requires

.PHONY : src/CMakeFiles/cooccurrence.dir/requires

src/CMakeFiles/cooccurrence.dir/clean:
	cd /home/jie/Desktop/vector_project/launch_computation_and_evaluation/tools/hpca-master/build/src && $(CMAKE_COMMAND) -P CMakeFiles/cooccurrence.dir/cmake_clean.cmake
.PHONY : src/CMakeFiles/cooccurrence.dir/clean

src/CMakeFiles/cooccurrence.dir/depend:
	cd /home/jie/Desktop/vector_project/launch_computation_and_evaluation/tools/hpca-master/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/jie/Desktop/vector_project/launch_computation_and_evaluation/tools/hpca-master /home/jie/Desktop/vector_project/launch_computation_and_evaluation/tools/hpca-master/src /home/jie/Desktop/vector_project/launch_computation_and_evaluation/tools/hpca-master/build /home/jie/Desktop/vector_project/launch_computation_and_evaluation/tools/hpca-master/build/src /home/jie/Desktop/vector_project/launch_computation_and_evaluation/tools/hpca-master/build/src/CMakeFiles/cooccurrence.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : src/CMakeFiles/cooccurrence.dir/depend

