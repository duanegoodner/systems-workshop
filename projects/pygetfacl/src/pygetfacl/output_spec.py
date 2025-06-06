from dataclasses import dataclass
from typing import Callable

# from .aclpath_exceptions import ExcessRegexMatches, InsufficientRegexMatches
# from .file_setting import (
#     FlagSetting,
#     PermissionSetting,
#     SpecialGroupPermission,
#     SpecialUserPermission,
# )

import pygetfacl.aclpath_exceptions as ae
import pygetfacl.file_setting as fs


@dataclass
class ItemFromGetFacl:
    """
    Specification for piece of information returned by a line in system
    getfacl output.
    attribute: Name used in ACLData class
    regex: string regex used to extract info from sys getfacl output
    file_setting_type: Enum corresponding to concrete implementation of
    FileSettingString
    required: bool indicating whether item must be present
    max_entries: int indicating max allowed items of this type in any data
    containers classes.
    """

    attribute: str
    regex: str
    required: bool
    max_entries: int | None
    acl_data_type: (
        Callable[..., str]
        | Callable[..., fs.FlagSetting]
        | Callable[..., fs.PermissionSetting]
        | Callable[..., fs.SpecialUserPermission]
        | Callable[..., fs.SpecialGroupPermission]
    )

    def validate_matches(self, matched_groups: list[str]):
        if (self.max_entries is not None) and (
            len(matched_groups) > self.max_entries
        ):
            raise ae.ExcessRegexMatches(
                self.attribute, len(matched_groups), self.max_entries
            )
        if self.required and len(matched_groups) < 1:
            raise ae.InsufficientRegexMatches(
                self.attribute, len(matched_groups)
            )

    def to_max_one_item_acl_format(self, matched_groups: list[str]):
        assert len(matched_groups) <= 1
        if len(matched_groups) == 0:
            return None
        else:
            return self.acl_data_type(matched_groups[0].strip())

    def to_multi_item_acl_format(self, matched_groups: list[str]):
        if len(matched_groups) == 0:
            return {}
        else:
            pairs = [item.split(":") for item in matched_groups]
            assert all([len(pair) == 2 for pair in pairs])
            return {
                name: self.acl_data_type(permission)
                for name, permission in pairs
            }

    def to_acl_constructor_format(self, matched_groups: list[str]):
        if self.max_entries == 1:
            return self.to_max_one_item_acl_format(matched_groups=matched_groups)
        else:
            return self.to_multi_item_acl_format(matched_groups=matched_groups)
        # if len(matched_groups) == 0:
        #     return None
        # if (len(matched_groups) == 1) and (self.max_entries == 1):
        #     return self.acl_data_type(matched_groups[0].strip())
        # else:
        #     pairs = [item.split(":") for item in matched_groups]
        #     assert all([len(pair) == 2 for pair in pairs])
        #     return {
        #         name: self.acl_data_type(permission)
        #         for name, permission in pairs
        #     }

    # def to_dict_entry(self, matched_groups: list[str]):
    #     if len(matched_groups) == 0:
    #         return None
    #     if (len(matched_groups) == 1) and (self.max_entries == 1):
    #         return matched_groups[0].strip()
    #     else:
    #         key_vals = [item.split(":") for item in matched_groups]
    #         assert all([len(pair) == 2 for pair in key_vals])
    #         return {key: value for key, value in key_vals}


def getfacl_output_items() -> list[ItemFromGetFacl]:
    """
    Provides output spec entry for each possible type of info from getfacl
    Returns:
        List of ItemFromGetFacl objects

    """
    return [
        ItemFromGetFacl(
            attribute="owning_user",
            regex="(?<=^# owner:).*$",
            required=True,
            max_entries=1,
            acl_data_type=str,
        ),
        ItemFromGetFacl(
            attribute="owning_group",
            regex="(?<=^# group:).*$",
            required=True,
            max_entries=1,
            acl_data_type=str,
        ),
        ItemFromGetFacl(
            attribute="flags",
            regex="(?<=^# flags:).*$",
            required=False,
            max_entries=1,
            acl_data_type=fs.FlagSetting.from_string,
        ),
        ItemFromGetFacl(
            attribute="user",
            regex="(?<=^user::).*$",
            required=True,
            max_entries=1,
            acl_data_type=fs.PermissionSetting.from_string,
        ),
        ItemFromGetFacl(
            attribute="special_users",
            regex="(?<=^user:)(?!:).*$",
            required=False,
            max_entries=None,
            acl_data_type=fs.PermissionSetting.from_string,
        ),
        ItemFromGetFacl(
            attribute="group",
            regex="(?<=^group::).*$",
            required=True,
            max_entries=1,
            acl_data_type=fs.PermissionSetting.from_string,
        ),
        ItemFromGetFacl(
            attribute="special_groups",
            regex="(?<=^group:)(?!:).*$",
            required=False,
            max_entries=None,
            acl_data_type=fs.PermissionSetting.from_string,
        ),
        ItemFromGetFacl(
            attribute="mask",
            regex="(?<=^mask::).*$",
            required=False,
            max_entries=1,
            acl_data_type=fs.PermissionSetting.from_string,
        ),
        ItemFromGetFacl(
            attribute="other",
            regex="(?<=^other::).*$",
            required=True,
            max_entries=1,
            acl_data_type=fs.PermissionSetting.from_string,
        ),
        ItemFromGetFacl(
            attribute="default_user",
            regex="(?<=^default:user::).*$",
            required=False,
            max_entries=1,
            acl_data_type=fs.PermissionSetting.from_string,
        ),
        ItemFromGetFacl(
            attribute="default_special_users",
            regex="(?<=^default:user:)(?!:).*$",
            required=False,
            max_entries=None,
            acl_data_type=fs.PermissionSetting.from_string,
        ),
        ItemFromGetFacl(
            attribute="default_group",
            regex="(?<=^default:group::).*$",
            required=False,
            max_entries=1,
            acl_data_type=fs.PermissionSetting.from_string,
        ),
        ItemFromGetFacl(
            attribute="default_special_groups",
            regex="(?<=^default:group:)(?!:).*$",
            required=False,
            max_entries=None,
            acl_data_type=fs.PermissionSetting.from_string,
        ),
        ItemFromGetFacl(
            attribute="default_mask",
            regex="(?<=^default:mask::)(?!:).*$",
            required=False,
            max_entries=1,
            acl_data_type=fs.PermissionSetting.from_string,
        ),
        ItemFromGetFacl(
            attribute="default_other",
            regex="(?<=^default:other::).*$",
            required=False,
            max_entries=1,
            acl_data_type=fs.PermissionSetting.from_string,
        ),
    ]
