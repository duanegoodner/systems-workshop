import pytest
import unittest.mock as mock
from pygetfacl.aclpath_exceptions import SubprocessException
from pygetfacl.subprocess_caller import SubProcessCaller


@pytest.fixture
def good_command_caller():
    return SubProcessCaller(command=["echo", "hello"])


@pytest.fixture
def bad_command_caller():
    return SubProcessCaller(command=["ls", "blahblah"])


class TestSubprocessCaller:

    def test_mocked_non_zero_return_code(self, good_command_caller):
        with mock.patch("subprocess.CompletedProcess") as MockCompletedProcess:
            MockCompletedProcess.return_value.returncode = 1

            with pytest.raises(SubprocessException):
                result = good_command_caller.call_with_stdout_capture()

    def test_good_command(self, good_command_caller):
        result = good_command_caller.call_with_stdout_capture()
        assert result.strip() == "hello"

    def test_bad_command(self, bad_command_caller):
        with pytest.raises(SubprocessException):
            result = bad_command_caller.call_with_stdout_capture()


