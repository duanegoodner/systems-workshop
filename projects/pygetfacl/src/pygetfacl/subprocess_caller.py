import subprocess
# from .aclpath_exceptions import SubprocessException
import pygetfacl.aclpath_exceptions as ae


class SubProcessCaller:
    """
    Handles details of a subprocess call.
    """
    def __init__(
        self,
        command: list[str],
    ):
        """
        Args:
            command: list of strings representing the command to be run
        Raises:
            SubprocessException if subprocess return code != 0
        """
        self._command = command

    def call_with_stdout_capture(self):
        """
        Calls subprocess in a way that will return standard out if subprocess
        return code == 0, and raise exception otherwise.
        Returns:
            string obtained from subprocess standard out
        """
        subprocess_result = subprocess.run(
            self._command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        if subprocess_result.returncode != 0:
            raise ae.SubprocessException(subprocess_result)

        return subprocess_result.stdout.decode("utf-8")
