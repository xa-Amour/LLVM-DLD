import os

from logger_factory import *
from singleton import Singleton


class HandleCompileCommandsJsonFile(object):
    __metaclass__ = Singleton

    def __init__(self, compilation_database_path):
        self.log = logging.info(
            self.__class__.__name__ + ' starts handling relative path files')
        self.compilation_database_path = compilation_database_path
        self._file_lst = []

    def gen_compile_commands_json_file(self):
        compile_commands_json = os.path.join(self.compilation_database_path, 'compile_commands.json').replace('\\',
                                                                                                              '/')
        if not os.path.exists(compile_commands_json):
            raise Exception('Could not find compile_commands.json file')

        with open(compile_commands_json, 'r') as fileReader:
            file_lst = []
            for line in fileReader.readlines():
                if '"file": ' in line:
                    file_lst.append(line.split(': ')[1].strip().strip('"'))
        return file_lst

    def __transform_abspath_parameters(self, compilation_database_path, file_lst):
        try:
            os.chdir(compilation_database_path)
        except Exception as e:
            e.args += ('Transform relative path parameters to absolute path parameters failed',)
            raise
        abs_path_file_lst = []
        for rel_path_file in file_lst:
            abs_path_file_lst.append(os.path.abspath(rel_path_file))
        assert len(file_lst) == len(abs_path_file_lst), 'Number of transform path element appers errors'
        return abs_path_file_lst

    def get_abs_file(self):
        import platform
        if platform.system() == "Windows":  # IS_WINDOWS
            self._file_lst = self.__transform_abspath_parameters(self.compilation_database_path,
                                                                 self.gen_compile_commands_json_file())
            print 'Number of file in [{0}] is : {1} '.format('compile_commands.json', len(self._file_lst))
            logging.info('HandleCompileCommandsJsonFile handles relative path files successfully')
            return self._file_lst