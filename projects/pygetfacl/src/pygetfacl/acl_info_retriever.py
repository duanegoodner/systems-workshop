from pathlib import Path
import pygetfacl.data_containers as dc
import pygetfacl.subprocess_caller as sc


class _ACLInfoRetriever:
    """
    Retrieves Access Control List info for its ._path data member
    """

    def __init__(self, path: str | Path):
        """
        Constructor
        :param path: The filepath that ACL info is retrieved for
        """
        if type(path) == str:
            self._path = Path(path)
        elif isinstance(path, Path):
            self._path = path
        else:
            raise TypeError

    def getfacl_raw(self) -> str:
        return sc.SubProcessCaller(
            # -E option --> don't show effective permissions
            # (calc'ing ep based on mask easier than parsing)
            command=["getfacl", "-E", str(self._path)]
        ).call_with_stdout_capture()

    def getfacl(self) -> dc.ACLData:
        """
        Gets ACL info for self._path
        :return: a :class: `ACLData` object
        """
        raw_output = self.getfacl_raw()

        return dc.ACLData.from_getfacl_cmd_output(raw_output)


def getfacl_raw(path: str | Path) -> str:
    return _ACLInfoRetriever(path).getfacl_raw()


def getfacl(path: str | Path) -> dc.ACLData:
    return _ACLInfoRetriever(path).getfacl()
