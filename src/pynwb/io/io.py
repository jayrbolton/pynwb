from abc import ABCMeta, abstractmethod
from .build import BuildManager
from .build import GroupBuilder
from ..core import docval, popargs, getargs
from ..file import NWBFile

class NWBReader(object, metaclass=ABCMeta):

    @abstractmethod
    @docval(returns='a GroupBuilder representing the NWB Dataset', rtype='GroupBuilder')
    def read_builder(self):
        ''' Read an NWB Dataset and return the GroupBuilder represention '''
        pass

class NWBWriter(object, metaclass=ABCMeta):

    @abstractmethod
    @docval({'name': 'builder', 'type': GroupBuilder, 'doc': 'the GroupBuilder object representing the NWBFile'})
    def write_builder(self, **kwargs):
        ''' Write a GroupBuilder representing an NWBFile object '''
        pass

class NWBIO(object, metaclass=ABCMeta):
    @docval({'name': 'manager', 'type': BuildManager, 'doc': 'the BuildManager to use for I/O', 'default': None})
    def __init__(self, **kwargs):
        self.__manager = getargs('manager', kwargs)
        if self.__manager is None:
            from pynwb.io import TYPE_MAP
            self.__manager = BuildManager(TYPE_MAP)
        self.__built = dict()

    @docval(returns='the NWBFile object', rtype=NWBFile)
    def read(self, **kwargs):
        f_builder = self.read_builder()
        nwb_file = self.__manager.construct(f_builder)
        return nwb_file

    @docval({'name': 'nwb_file', 'type': NWBFile, 'doc': 'the NWBFile object to write'})
    def write(self, **kwargs):
        nwb_file = getargs('nwb_file', kwargs)
        f_builder = self.__manager.build(nwb_file)
        self.write_builder(f_builder)

    @abstractmethod
    @docval(returns='a GroupBuilder representing the NWB Dataset', rtype='GroupBuilder')
    def read_builder(self):
        ''' Read an NWB Dataset and return the GroupBuilder represention '''
        pass

    @abstractmethod
    @docval({'name': 'builder', 'type': GroupBuilder, 'doc': 'the GroupBuilder object representing the NWBFile'})
    def write_builder(self, **kwargs):
        ''' Write a GroupBuilder representing an NWBFile object '''
        pass
