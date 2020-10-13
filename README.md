# DLD
DeadLock Detection

## About
This demo is to detect dead lock in C/C++ source code and not involve any business logic to the greatest extent

## Method
* First step: acquire all thread identities in project
* Second step: analyze the call path of threads based on first step
* Third step: directed graph ring detection of threads call

## Module Invocation Diagram
* As picture module_invocation_diagram

## Keywords
* Python2.7
* LLVM (Low Level Virtual Machine)
* clang
* libclang
* Mongodb