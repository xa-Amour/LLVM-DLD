from const import *

try:
    from worker_identity_filter import worker_identity_dict
    from detect_worker_call_path import worker_chain_lst
except ImportError as e:
    e.args += ('Import worker_identity_dict or worker_chain_lst failed',)
    raise


class ProduceGraphData(object):
    '''
    Process the path of worker calls to generate source data that can build directed graphs.
    '''
    __metaclass__ = Singleton

    def __init__(self, worker_chain_lst, worker_identity_dict):
        self.worker_chain_lst = worker_chain_lst
        self.worker_identity_dict = worker_identity_dict

    def __gen_whole_call_pairs(self, worker_call_pairs_lst, worker_identify_dict):
        '''Generate the full arrangement of worker call pairs according to worker's different identity'''

        def replace_identity_by_element_name(pairs_lst, identify_dict):
            '''Replace by worker identify based on the element name '''

            def tuple_to_list(lst):
                for i in xrange(len(lst)):  # Convert the tuple element in the list to a list, readable and writable
                    if isinstance(lst[i], tuple):
                        lst[i] = list(lst[i])
                    else:
                        raise ValueError('element should be a tuple')
                return lst

            pairs_lst = tuple_to_list(pairs_lst)
            for i in xrange(len(pairs_lst)):
                for j, _ in enumerate(pairs_lst[i]):
                    if pairs_lst[i][j] in identify_dict.keys():
                        pairs_lst[i][j] = worker_identify_dict[pairs_lst[i][j]]
            return pairs_lst

        def lsts_combination(lsts):
            '''
            Enter a list of lists, and output all possible permutations and
            combinations of all elements in each list
            '''
            try:
                import reduce
            except:
                from functools import reduce

            def comb_func(lst1, lst2):
                return [(str(i), str(j)) for i in lst1 for j in lst2]

            return reduce(comb_func, lsts)

        worker_lst = []
        for i in replace_identity_by_element_name(worker_call_pairs_lst, worker_identify_dict):
            tmp = lsts_combination(i)
            for j in tmp:
                worker_lst.append(j)

        return {}.fromkeys(worker_lst).keys()

    def __gen_worker_identify(self, worker_identity_dict):
        '''
        Generate a dictionary of worker corresponds to different identities
        '''
        worker_identify_dict = {}
        for k, v in worker_identity_dict.items():
            worker_identify_lst = []
            for i in v['worker_identity'].values():
                worker_identify_lst += i
            worker_identify_dict[k] = {}.fromkeys(worker_identify_lst).keys()
        return worker_identify_dict

    def __pretreat_worker_call(self, worker_chain_lst):
        '''Preprocessing worker_chain_lst, including split thread call pairs, de-duplication'''

        existent_worker_lst = [worker_item.get('worker_name', None) for worker_item in worker_identity_dict.values()]

        def del_specific_element(path_lst):
            for i in xrange(len(path_lst)):
                for j, _ in enumerate(path_lst[i]):
                    path_lst[i][j] = path_lst[i][j].split(':')[0]
                    if path_lst[i][
                        j] not in existent_worker_lst:  # remove the 'sync_call' element from the list
                        path_lst[i][j] = const.SYNC_FLAG
                path_lst[i] = filter(lambda x: x != const.SYNC_FLAG, path_lst[i])
            return path_lst

        single_call_pairs_lst = []

        for item_lst in del_specific_element(worker_chain_lst):
            single_call_pairs = zip(item_lst, item_lst[
                                              1:])
            for pairs in single_call_pairs:
                single_call_pairs_lst.append(pairs)
        return {}.fromkeys(single_call_pairs_lst).keys()

    def produce_graph_data(self):
        return {}.fromkeys(self.__gen_whole_call_pairs(self.__pretreat_worker_call(self.worker_chain_lst),
                                                       self.__gen_worker_identify(self.worker_identity_dict))).keys()