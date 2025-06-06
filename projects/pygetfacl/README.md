# pygetfacl

*Pygetfacl* retrieves Access Control List (ACL) information provided by the Linux [`getfacl`](https://manpages.ubuntu.com/manpages/trusty/man1/getfacl.1.html) command and stores that information as a Python object.



## System Requirements

* Linux distribution with the `acl` package installed.
* Python version 3.7 or higher



## Primary Use Case

*Pygetfacl* may be useful any time you want to obtain a file path's ACL information from within a Python program.



## Installation

From the command line:
```shell
$ pip install git+https://github.com/duanegoodner/pygetfacl
```



## Basic Usage

> **Note**
> If you want to test pygetfacl in Docker, you can build and run a container using files provided in the `demo_docker` directory. From the pygetfacl project root directory, run the following terminal commands to build/run the container and start a `bash` shell inside it. Pygetfacl is installed during the image build process.
>
> ```shell
> $ docker build ./demo_docker -t pygetfacl_demo
> $ docker run -it -d --rm --name="pygetfacl_demo" pygetfacl_demo
> $ docker exec -it -w /home/user_a pygetfacl_demo /bin/bash
> ```

From the command line (either in your local environment, or a Docker container), run the following command to create a test directory with some interesting ACL settings, and start the Python interpreter in interactive mode.
```shell
$ mkdir test_dir \
  && sudo useradd user_b \
  && setfacl -bn test_dir \
  && setfacl -m u:user_b:rwx test_dir \
  && chmod g+s test_dir \
  && python
```

Then, in the Python interpreter, run the following commands to get a feel for `pygetfacl.getfacl()` and the `ACLData` object that it returns: 
```pycon
>>> import pygetfacl
>>> acl_data = pygetfacl.getfacl("test_dir")
>>> import pprint
>>> pprint.pprint(acl_data)
ACLData(owning_user='user_a',
        owning_group='user_a',
        flags=-s-,
        user=rwx,
        special_users={'user_b': rwx},
        group=r-x,
        special_groups=None,
        mask=rwx,
        other=r-x,
        default_user=None,
        default_special_users=None,
        default_group=None,
        default_special_groups=None,
        default_mask=None,
        default_other=None)
```

The effective permissions can be accessed via the `.effective_permissions` property of the ACLData object returned by `pygetfacl.getfacl`.

```
>>> print(acl_data.effective_permissions)
user: rwx
special_users: {'user_b': rwx}
group: r-x
special_groups: None
other: r-x
default_user: None
default_special_users: None
default_group: None
default_special_groups: None
default_other: None
```

Permissions and flags in an ACLData object have \__repr__ methods defined so they print in the usual string form when printed (e. g. `rwx` or `sst`), but the value of each bit is stored as a boolean in a private data member that can be accessed with a public getter.

```pycon
>>> special_user_effective = acl_data.effective_permissions.special_users
>>> user_b_effective = special_user_effective.get("user_b")
>>> print(user_b_effective)
rwx
>>> vars(user_b_effective)
{'_r': True, '_w': True, '_x': True}
>>> print(f"user_b effective permissions: r = {user_b_effective.r}, w = {user_b_effective.w}, x = {user_b_effective.x}")
user_b effective permissions: r = True, w = True, x = True
```



## Limitations

*Pygetfacl* does not offer any methods for changing ACL settings (or even "regular" permission ). For that, you may want to look at:
* [pylibacl](https://pypi.org/project/pylibacl/)
* [miracle-acl](https://pypi.org/project/miracle-acl/)
* [trigger.acl](https://pythonhosted.org/trigger/api/acl.html#module-trigger.acl)
* the standard library [`pathlib.Path.chmod()`](https://docs.python.org/3/library/pathlib.html#pathlib.Path.chmod) or [`os.chmod()`](https://docs.python.org/3/library/os.html#os.chmod) methods (for "regular" permissions only)
* calling the necessary system commands using the standard library [subprocess](https://docs.python.org/3/library/subprocess.html) module. This option usually works well for me, perhaps because my use cases tend to be simple.



## Project Status

*Pygetfacl* is a work-in-progress. Will use it as a dependency in other projects and modify as improvement opportunities arise.

  