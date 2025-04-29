CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra -pedantic

all: js2py js2py_specific

js2py: final_solution.cpp
	$(CXX) $(CXXFLAGS) -o js2py final_solution.cpp

js2py_specific: final_version.cpp
	$(CXX) $(CXXFLAGS) -o js2py_specific final_version.cpp

clean:
	rm -f js2py js2py_specific *.o

.PHONY: all clean 