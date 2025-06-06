import pytest
from pygetfacl.data_containers import ACLData, EffectivePermissions
import pygetfacl.file_setting as fs


@pytest.fixture
def example_system_getfacl_result():
    return (
        "# file: pygetfacl_test_dir\n"
        "# owner: user_a\n"
        "# group: user_a\n"
        "user::rwx\n"
        "user:pygetfacl_test_user:rwx\n"
        "group::r-x\n"
        "group:pygetfacl_test_group:rw-\n"
        "mask::rwx\n"
        "other::r-x\n"
        "default:user::rwx\n"
        "default:group::rwx\n"
        "default:other::r-x\n"
        "\n"
    )


@pytest.fixture
def example_acl_data(example_system_getfacl_result):
    return ACLData.from_getfacl_cmd_output(example_system_getfacl_result)


class TestACLData:
    def test_from_getfacl_cmd_output(self, example_system_getfacl_result):
        my_acl_data = ACLData.from_getfacl_cmd_output(
            example_system_getfacl_result
        )
        assert my_acl_data.owning_user == "user_a"
        assert my_acl_data.owning_group == "user_a"
        assert my_acl_data.flags is None
        # compare against str(PermissionSetting) when not part of dict or list
        assert str(my_acl_data.user) == "rwx"
        assert str(my_acl_data.group) == "r-x"
        assert str(my_acl_data.other) == "r-x"
        assert str(my_acl_data.mask) == "rwx"
        assert my_acl_data.special_users == {
            "pygetfacl_test_user": fs.PermissionSetting(r=True, w=True, x=True)
        }
        assert my_acl_data.special_groups == {
            "pygetfacl_test_group": fs.PermissionSetting(
                r=True, w=True, x=False
            )
        }
        assert my_acl_data.default_special_groups == {}
        assert my_acl_data.default_special_users == {}

        assert str(my_acl_data.default_user) == "rwx"
        assert str(my_acl_data.default_group) == "rwx"
        assert str(my_acl_data.default_other) == "r-x"


class TestEffectivePermissions:

    def test_effective_permissions_init(self, example_acl_data):
        ep = EffectivePermissions(example_acl_data)
        assert str(ep.user) == "rwx"
        assert str(ep.group) == "r-x"
        assert str(ep.other) == "r-x"
        assert str(ep.default_user) == "rwx"
        assert str(ep.default_group) == "rwx"
        assert str(ep.default_other) == "r-x"
        assert ep.special_users == {
            "pygetfacl_test_user": fs.PermissionSetting(r=True, w=True, x=True)
        }
        assert ep.special_groups == {
            "pygetfacl_test_group": fs.PermissionSetting(
                r=True, w=True, x=False
            )
        }
        assert ep.default_special_groups == {}

        assert ep.default_special_users == {}

        print("debugger break point")



