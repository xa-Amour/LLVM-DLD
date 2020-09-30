import os
import platform

import ccsyspath

import clang.cindex
from clang.cindex import *
from logger_factory import *
from singleton import Singleton

if platform.system() == "Windows":  # IS_WINDOWS
    libclang_path = r'C:\Program Files\LLVM\bin\libclang.dll'
    if not os.path.exists(libclang_path):
        raise Exception("Please install clang with libclang.dll")
elif platform.system() == "Darwin":  # IS_MAC
    libclang_path = '/Library/Developer/CommandLineTools/usr/lib/libclang.dylib'
    pipe = os.popen('mdfind -name "libclang.dylib"').readlines()
    if not pipe:
        raise Exception("Please install clang with libclang.dylib")
elif platform.system() == "Linux":  # IS_LINUX
    libclang_path = '/usr/lib/llvm-7.0/lib/libclang-7.0.so.1'
    if not os.path.exists(libclang_path):
        raise Exception("Please install clang with libclang.so")

if Config.loaded == True:
    pass
else:
    Config.set_library_file(libclang_path)

syspath = ccsyspath.system_include_paths('clang++')
incargs = [b'-I' + inc for inc in syspath]
args = '-x c++ -v'.split() + incargs

current_path = os.path.abspath(os.path.dirname(__file__))


class GenDependentParametersByCdb(object):

    def __init__(self, compilation_database_path, source_file_path):
        self.log = logging.info(
            self.__class__.__name__ + ' starts handling ' + source_file_path + 'dependent parameters')
        self._args = []
        self.args = args
        self.args_lst = 'args_lst.txt'
        self.compilation_database_path = compilation_database_path
        self.source_file_path = source_file_path
        self.compdb = clang.cindex.CompilationDatabase.fromDirectory(compilation_database_path)

    def __handle_dependent_parameters(self):
        file_args = self.compdb.getCompileCommands(self.source_file_path)
        try:
            arguments = list(iter(file_args).next().arguments)  # Same arguments as "compile_commands.json" generated
        except Exception as e:
            e.args += ('Iter parameter from CompilationDatabase failure',)
            raise
        clang_args = self.args + arguments
        clang_args.remove('clang-cl.exe')
        arguments_lst = []
        for argument in clang_args:
            if argument.startswith('-D') or argument.startswith('-I'):
                arguments_lst.append(argument)
        try:
            os.chdir(self.compilation_database_path)
        except Exception as e:
            e.args += ('Could not chdir to compilation database path ',)
            raise
        return arguments_lst

    def get_args(self):
        if platform.system() == "Windows":  # IS_WINDOWS
            self._args = self.__handle_dependent_parameters()
            with open(self.args_lst, 'w') as fileWriter:
                for arg in self._args:
                    fileWriter.write(arg + '\n')
            logging.info('GenDependentParametersByCdb handles {0} dependent parameters successfully'.format(
                self.source_file_path))
            print 'Number of args in [{0}] is : {1} '.format(self.source_file_path, len(self._args))
            return self._args


class GenDependentParametersManual(object):
    __metaclass__ = Singleton

    global build_ninja_location

    def __init__(self):
        self.log = logging.info(self.__class__.__name__ + ' starts handling dependent parameters')
        self.syspath = syspath
        self.incargs = incargs
        self.args = args
        self.ARGS = ''
        self.compile_commands_json = 'compile_commands.json'
        self.args_lst = 'args_lst.txt'

    def __acquire_compile_commands_json(self):
        global build_ninja_location

        if platform.system() == "Windows":  # IS_WINDOWS
            with os.popen('aclient --agora gen win x64 debug ') as pipe:
                if 'Done.' in pipe.read():
                    build_ninja_location = os.path.dirname(os.path.realpath(__file__)).replace('\\',
                                                                                               '/') + '/build/win/x64/'
                    if os.path.exists(build_ninja_location):
                        with os.popen('ninja -C {0} -t compdb cc cxx asm objc objcxx > compile_commands.json'.format(
                                build_ninja_location)) as pipe_sec:  # Note that should use format() to handle popen() arguments with system path
                            print pipe_sec.read()
                            if os.path.exists('compile_commands.json'):
                                return True
                else:
                    return False
        elif platform.system() == "Darwin":  # IS_MAC
            pass
        elif platform.system() == "Linux":  # IS_LINUX
            pass

    def __handle_dependent_parameters(self, file):
        if not os.path.exists(file):
            raise Exception('No such dependent parameters file !!!')
        with open(file, 'r') as fileReader:
            parameters_lst = []
            for line in fileReader.readlines():
                if '"command":' in line:
                    command_lst = line.split()
                    for argument in command_lst:
                        if argument.startswith('-D') or argument.startswith('-I'):
                            parameters_lst.append(argument)
        parameters_lst = {}.fromkeys(parameters_lst).keys()  # Remove duplicate elements
        return parameters_lst

    def __transform_abspath_parameters(self, file_location, command_lst):
        try:
            os.chdir(file_location)
        except Exception as e:
            e.args += ('Transform relative path parameters to absolute path parameters failed ',)
            raise
        transform_command_lst = []
        for argument in command_lst:
            if argument.startswith('-I'):
                transform_argument = '-I' + os.path.abspath(argument[2:]).replace('\\',
                                                                                  '/')  # # Note that it should replace '\\' with '/', otherwise you will make a mistake during passing parameters to args in index.parse()
                transform_command_lst.append(transform_argument)
            else:
                transform_command_lst.append(argument)
        assert len(transform_command_lst) == len(command_lst), 'Number of transform command element appers errors'
        try:
            os.chdir(current_path)
        except Exception as e:
            e.args += ('Chdir to current path failed ',)
            raise
        return transform_command_lst

    def get_args(self):
        if platform.system() == "Windows":  # IS_WINDOWS
            try:
                if self.__acquire_compile_commands_json() is True:
                    command_lst = self.__handle_dependent_parameters(self.compile_commands_json)
                    self.ARGS = self.__transform_abspath_parameters(build_ninja_location, command_lst) + self.args
                    with open(self.args_lst, 'w') as fileWriter:
                        for arg in self.ARGS:
                            fileWriter.write(arg + '\n')
                    logging.info('GenDependentParameters handles dependent parameters successfully')
                    print 'Number of args: ', len(self.ARGS)
                    return self.ARGS
            except Exception as e:
                e.args += ('Generate dependent parameters failed ',)
                raise
        elif platform.system() == "Darwin":  # IS_MAC
            pass
        elif platform.system() == "Linux":  # IS_LINUX
            pass
