# Summer 2024 Development Outline 

## Housekeeping
 * Move Generator repos from 415 org to F23 org
 * ~~Move SCalc repos from 415 org into F23 org~~ [DONE]
 * Rebrand Ayrtons teams Gazprea as solution.
 * Assign2 conversion for HW

## 415 Solutions
* Update Gazprea solution to reflect newest LLVM Version (18.X)
    * Opaque pointers
* Remove NULL and Identity types from the language spec and solution.

## Documentation Updates
 * Reference Compile and Runtime error types, where relevent, throughout docs. 
 * ~~Update for CLion lisence changes~~  [DONE] 
 * ~~0^0 should be undefined in docs.~~ [DONE]

## Totorials / New Docs
 * CMake tutorial
 * Docs and implementation examples for suggested/expected optimziations.
 * Formalize plan for meeting notes / communication requirements.

## Tester
 * Port existing solution tests to new test format
 * Add comments to Solution and Base repos for assigments
 * ~~Setup CI for new tests~~ [DONE] 
 * ~~Replace complex testfinding with simple implementation~~ [DONE]
 * Replace old CSV infra with one that can:
    - Trace execution times
    - Mark each toolchain separately (The SCalc one fail problem)

 * ~~Add state to testfile parsing to detect spec violations before they occur~~ [DONE]
 * Create open Gazprea TestSuite for speed (Optimization marks)

## Undecided / Miscelaneous Tasks
 * Rework VCalc vectors to be more ammenible to compile time construction.
 * CI QOL improvements
 * Gazprea Fuzzer
