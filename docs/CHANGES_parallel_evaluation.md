# Changes: Parallel Evaluation

**Original Author**: Ben Spencer  
**Document Type**: Design specification and implementation plan  
**Status**: Historical document from Python 2 development

**AIM:** Allow running tests in parallel.

This document represents Ben Spencer's design planning for implementing parallel test evaluation in the original system. While not fully implemented in the original Python 2 version, these concepts have influenced the modern Python 3 architecture.

## User Perspective

### New Configuration Option: `parallel`

We can set this to either:
1. **Number of parallel tests** - Each test would be assigned a number from 0..N as its "name"
2. **Names of each parallel test** - One test can be run in parallel for each name given

The idea of the names/numbers is that a test will need to know which one of the parallel threads it is, so it can behave appropriately. For example, in CUDA, the programmer would want to use `cudaSetDevice()` to choose one of the possible GPUs to use.

### Test Command Integration

The parallel "name" would be available as a substitution into the test command, such as `%%PARALLEL%%`. This is used to tell the test which thread it should be on. It may be ignored/not used.

### Test Distribution Strategy

**Question:** How are tests split into the separate threads?

**Idea 1:** Compile all tests, add the 'test' commands to one large pool, run these in parallel until they are all finished, then clean all the tests.

**Idea 2:** All tests are put into a pool, each parallel thread compiles a test, runs it the necessary number of times, then cleans it. All work for each test is performed together by a single thread.

*I think the second of these is the most sensible.*

## Developer Perspective

There are two main options for parallelizing the testing:

### Option 1: Multi-threaded Python Program

- Spawn the necessary number of Python threads
- Each thread deals with a certain test
- When done, the thread could either:
  - Begin working on a new test, or
  - End, and the system will spawn a new thread as needed

### Option 2: Background Process Spawning

- Use the subprocess module to create test processes without waiting for termination
- Create the required number of test processes
- Check when they finish and spawn new ones as necessary
- This seems a sensible match for 'Idea 1' above

*I prefer Option 2 - the tuner itself doesn't need to be multi-threaded, it only needs to spawn some independent tests without waiting for the previous ones to finish. We should simply have a maximum number of tests which can be running at once which the tuner will need to honor.*

## Implementation Plan

### Proposed Workflow:

1. **Compile all tests**
2. **Add all tests to be run to a pool** (including repetitions)
3. **Spawn the first N subprocesses**
4. **Wait for one to finish** (using `.poll()` and checking `.returncode`)
5. **When one finishes:** log that result and spawn another test from the pool
6. **Keep a vector of timers** which correspond to the vector of tests
7. **When all tests are finished:** run cleanup

This approach allows for efficient parallel execution while maintaining proper resource management and result tracking.