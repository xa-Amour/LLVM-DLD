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


## Module function details
    1、cycle_detection.py (Entrance).................Cycle detection of graph

    2、gen_dependent_parameter.py....................Handle the parameter dependencies that need to be imported for the clang parse file

    3、handle_compile_json_file.py...................Process compile json files from ninja

    4、gen_ast_by_Cdb.py.............................Get the abstract syntax tree from the compile database

    5、capture_worker_ownership.py...................To get the worker identity from the compilation json file

    6、detect_worker_call_path.py....................Detect the thread invocation path in the project

    7、worker_identity_dao.py........................Database interface design

    8、worker_identity_filter.py.....................Filter into useful worker identity information

    9、produce_graph_data.py.........................Process data into graphs

    10、logger_factory.py............................Logger factory design to define some log levels expediently

    11、singleton.py.................................Singleton design

    12、const.py.....................................Constant module

    13、thread_pool.py...............................Maybe we can extend the LLVM_customized_check plug-in with thread pools


## In future
Due to the limited knowledge, the deadlock detection tool still faces some shortcomings and deficiencies as well as areas that can be improved. However, it is now possible to form a closed loop for running detection, and it is hoped that it can be continuously improved in the future.

    1、As for the efficiency of the tool, it takes about seven or eight seconds for a file to be parsed. However, there are about four thousand files in the compiled file of our project, so it takes too long to detect once. I haven't investigated a good solution yet, but the direction is to see if Clang has a way to filter out some of the standard library code without detecting it, which would greatly reduce the runtime.

    2、The acquisition of thread identity ownership is not always 100% complete. The current approach is to do a cumulative template for each situation that already exists in the code, and then iterate if a new situation occurs later.

    3、You can then use thread pools or concurrency to manage modules that do not have dependencies, increasing the efficiency of the tool.


## Note:
Since this tool is written according to the CI environment of the SDK project team, please organize the files for use according to the following directory structure
Or it can be contacted before use: fightingxa@163.com

-- xxx_sdk_script (for all the build scripts)

    |-- xxx_engine2 (webrtc and some company customized components)

    |-- xxx_sdk3 (major company SDK repo)

    |-- xxx_sdk3_private (network related)

    |-- xxx_player (xxx player static lib)

    |-- xxx_sdk_tools

         |-- dead_lock
