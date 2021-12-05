from abc import abstractmethod
import os
from functools import lru_cache

cache = lru_cache(None)


class ResourcesBase:
    @abstractmethod
    def respath(self, resname: str) -> str:
        pass
    
    @abstractmethod
    def resdir(self) -> str:
        pass

    @cache
    def text(self, resname: str) -> str:
        with open(self.respath(resname), "r") as f:
            return f.read()

    @cache
    def binary(self, resname: str) -> bytes:
        with open(self.respath(resname), "rb") as f:
            return f.read()


class Resources(ResourcesBase):
    """
    Resources relative to module directory.

    Usage:

        resources = Resources(__file__)

    """

    def __init__(self, f: str, ) -> None:
        dir, rest = os.path.split(os.path.abspath(f))
        self._dir = dir

    def respath(self, resname: str) -> str:
        return f"{self._dir}/{resname}"
    
    def resdir(self) -> str:
        return self._dir


class ModuleResources(ResourcesBase):
    """
    Resources relative to `res/{module}`.

    Usage:

        module_resources = ModuleResources(__file__)

    """

    def __init__(self, f: str, ) -> None:
        dir, file = os.path.split(os.path.abspath(f))
        self._dir = dir
        module, _ = os.path.splitext(file)
        self._module = module

    def respath(self, resname: str) -> str:
        return f"{self._dir}/res/{self._module}/{resname}"
    
    def resdir(self) -> str:
        return f"{self._dir}/res/{self._module}"


class UninitializedResources(ResourcesBase):
    """
    An uninitialized resources object signals that something is wrong.
    """
    def __init__(self, error_msg) -> None:
        self._error_msg = error_msg

    def respath(self, resname: str) -> str:
        raise RuntimeError(self._error_msg)
    
    def resdir(self) -> str:
        raise RuntimeError(self._error_msg)
