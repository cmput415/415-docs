# All grammars in the base directory and grammars folder.
GRAMMARS:=$(wildcard *.g4)

# Construct the list of generated cpp file suffixes.
RESULT_CPP:=BaseListener Listener BaseVisitor Visitor Lexer Parser
RESULT_CPP:=$(foreach file, $(RESULT_CPP), $(file).cpp $(file).h)

# Construct the list of all generated file suffixes.
RESULT_BASES:=$(RESULT_CPP) .interp .tokens Lexer.interp Lexer.tokens

# We'll generate these files in a gen dir.
GEN_DIR:=${CURDIR}/gen/

# Construct the list of all generated files and also a filtered cpp/h only
# list.
GEN_RESULTS:= \
	$(foreach grammar, $(GRAMMARS:%.g4=%), \
		$(foreach base, $(RESULT_BASES), $(GEN_DIR)$(grammar)$(base)))
GEN_RESULTS_CPP:= $(filter %.cpp %.h, $(GEN_RESULTS))

# Get the ANTLR install location.
ANTLRI:=${ANTLR_INS}/include/antlr4-runtime/
ANTLRS:=${ANTLR_INS}/lib/libantlr4-runtime.a

# Get all of our source files.
SRC_CPP:=$(addprefix ${CURDIR}/, $(wildcard *.cpp *.h *.hpp))

# These targets produce nothing.
.PHONY: all clean

# Notify that these are not files to destroy. They are treated as
# "intermediates" otherise.
.PRECIOUS: $(GEN_RESULTS)

# We want to make our tool.
all: tool

echo:
	$(foreach result, $(RESULT_BASES), $(GEN_DIR)%$(result))

# How to build our tool. Depend on (RESULT_CPP).o first, then (SRC_CPP).
# We depend on the .h files to get updates, but there's no rule to build them.
# We'll filter out only the .o files to build.
tool: $(GEN_RESULTS_CPP:.cpp=.o) $(SRC_CPP:.cpp=.o)
	c++ -std=gnu++11 -Wall \
		$(filter %.o, $^) $(ANTLRS) \
		-I"$(ANTLRI)" -I"$(GEN_DIR)" \
		-o tool

# How to build files in the current directory.
%.o: %.cpp
	c++ -std=gnu++11 -Wall -I"$(ANTLRI)" -I"$(GEN_DIR)" -c "$<" -o "$@"

# How to generate files from a grammar.
$(foreach result, $(RESULT_BASES), $(GEN_DIR)%$(result)): %.g4
	java -Xmx500M org.antlr.v4.Tool \
		-Dlanguage=Cpp -listener -visitor \
		-o "$(GEN_DIR)" "$<"

# How to generate object files for the generated cpp files.
$(GEN_DIR)%.o: $(GEN_DIR)%.cpp
	c++ -std=gnu++11 -Wall -I"$(ANTLRI)" -I"$(GEN_DIR)" -c "$<" -o "$@"

# How to clean up
clean:
	rm -rf *.o "$(GEN_DIR)" tool
