from pygetfacl.aclpath_exceptions import InvalidFileSettingString
from dataclasses import dataclass


def validate_bit_string(
    bit_string: str,
    all_bits_set_repr: str,
    no_bits_set_repr: str,
    required_length: int,
):
    if (
        (not len(bit_string) == required_length)
        or (not len(all_bits_set_repr) == required_length)
        or (not len(no_bits_set_repr) == required_length)
        or (
            not all(
                [
                    (bit_string[i] == all_bits_set_repr[i])
                    or (bit_string[i] == no_bits_set_repr[i])
                    for i in range(len(bit_string))
                ]
            )
        )
    ):
        raise InvalidFileSettingString(
            value=bit_string,
            all_bits_set=all_bits_set_repr,
            no_bits_set=no_bits_set_repr,
        )
    # except AssertionError:
    #     raise InvalidFileSettingString


class PermissionSetting:
    def __init__(self, r: bool, w: bool, x: bool):
        self._r = r
        self._w = w
        self._x = x

    def __eq__(self, other):
        return all(
            [self._r == other.r, self._w == other.w, self._x == other.x]
        )

    def __repr__(self):
        r_char = "r" if self._r else "-"
        w_char = "w" if self._w else "-"
        x_char = "x" if self._x else "-"
        return f"{r_char}{w_char}{x_char}"

    @property
    def r(self) -> bool:
        return self._r

    @property
    def w(self) -> bool:
        return self._w

    @property
    def x(self) -> bool:
        return self._x

    @classmethod
    def from_string(cls, permission_string: str):
        validate_bit_string(
            bit_string=permission_string,
            all_bits_set_repr="rwx",
            no_bits_set_repr="---",
            required_length=3,
        )
        r = permission_string[0] == "r"
        w = permission_string[1] == "w"
        x = permission_string[2] == "x"
        return cls(r=r, w=w, x=x)


def compute_effective_permissions(
    base: PermissionSetting, mask: PermissionSetting
):
    if base is None:
        return None
    if mask is None:
        return base
    return PermissionSetting(
        r=(base.r and mask.r), w=(base.w and mask.w), x=(base.x and mask.x)
    )


class FlagSetting:
    def __init__(self, uid: bool, gid: bool, sticky: bool):
        self._uid = uid
        self._gid = gid
        self._sticky = sticky

    def __repr__(self):
        uid_char = "s" if self._uid else "-"
        gid_char = "s" if self._gid else "-"
        sticky_char = "t" if self._sticky else "-"
        return f"{uid_char}{gid_char}{sticky_char}"

    @classmethod
    def from_string(cls, flag_string: str):
        validate_bit_string(
            bit_string=flag_string,
            all_bits_set_repr="sst",
            no_bits_set_repr="---",
            required_length=3,
        )
        uid = flag_string[0] == "s"
        gid = flag_string[1] == "s"
        sticky = flag_string[2] == "t"
        return cls(
            uid=uid,
            gid=gid,
            sticky=sticky,
        )

    @property
    def uid(self) -> bool:
        return self._uid

    @property
    def gid(self):
        return self._gid

    @property
    def sticky(self):
        return self._sticky


@dataclass
class SpecialUserPermission:
    username: str
    permissions: PermissionSetting

    @classmethod
    def from_str_str_pair(cls, username: str, permission_string: str):
        permission_setting = PermissionSetting.from_string(
            permission_string=permission_string
        )
        return cls(username=username, permissions=permission_setting)


@dataclass
class SpecialGroupPermission:
    group_name: str
    permissions: PermissionSetting

    @classmethod
    def from_str_str_pair(cls, group_name: str, permission_string: str):
        permission_setting = PermissionSetting.from_string(
            permission_string=permission_string
        )
        return cls(group_name=group_name, permissions=permission_setting)
