# Summer 2024 Development Outline 

These are points summarized from Quinn's doccument, Nelson and I's document and the inital
meeiting on 02/05/2024. Pleae add, update or remove points as seen fit :)  

## Housekeeping
- [] Move student Generator and SCalc repos from 415 org into F23 org
- [] Rebrand Ayrtons teams Gazprea as solution.
- [] Assign2 conversion for HW

## Software Versioning
Update documentation and Base projects to reflect the following:
- [] LLVM 16.0.6 -> 17.0.7
- [] GCC >= 7.1 & Clang >= 5.0 (Per LLVM 17.X requirement)
- [] CMake >= 3.20.0 (Per LLVM 17.X requirement)

## Documentation Updates
- [] Update for CLion lisence changes  
- [] Reference Compile and Runtime error types, where relevent, throughout docs. 
- [] UML Diagram on SCalc as per Quinns notes.
- [] 0^0 should be undefined in docs.

## Totorials / New Docs
- [] CMake tutorial
- [] Docs and implementation examples for suggested/expected optimziations.

## Tester
- [] Decide whether or not to proceed with LLVM Filecheck 
- [] Collect execution timings from each test.
- [] Add mutlithreading -- if old tester is not replaced with Filecheck.
- [] Competative testing framework for program SPEED.
- [] Couple TA tests for specific optimizations.

## Miscelaneous
- [] Rework VCalc vectors to be more ammenible to compile time construction.
- [] CI QOL improvements
- [] Gazprea Fuzzer
- [] Formalize plan for meeting notes / communication requirements.
- [] Gazprea Reference parser or even Gazprea CML 
