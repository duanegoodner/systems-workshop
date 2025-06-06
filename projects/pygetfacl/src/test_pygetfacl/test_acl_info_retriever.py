from pathlib import Path
import os
import pygetfacl
import pytest
import subprocess


@pytest.fixture
def temp_dir_with_some_facl_settings(tmp_path) -> Path:
    my_dir = tmp_path / "test_dir"
    my_dir.mkdir()
    subprocess.check_call(["setfacl", "-bn", str(my_dir)])
    subprocess.check_call(
        ["setfacl", "-m", f"u:{os.getlogin()}:rwx", str(my_dir)]
    )
    subprocess.check_call(["setfacl", "-d", "-m", "g::rwx", str(my_dir)])
    subprocess.check_call(["chmod", "g+s", str(my_dir)])

    yield my_dir


def test_getfacl(temp_dir_with_some_facl_settings):
    result = pygetfacl.getfacl(temp_dir_with_some_facl_settings)


def test_getfacl_raw(temp_dir_with_some_facl_settings):
    pygetfacl.getfacl_raw(temp_dir_with_some_facl_settings)
