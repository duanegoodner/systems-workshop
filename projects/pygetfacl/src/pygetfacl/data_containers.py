import pprint
import re
from dataclasses import dataclass, field

import pygetfacl.file_setting as fs
import pygetfacl.output_spec as osp


# not using @dataclass b/c want to calc effective permissions in constructor
@dataclass
class ACLData:
    owning_user: str
    owning_group: str
    flags: fs.FlagSetting
    user: fs.PermissionSetting
    group: fs.PermissionSetting
    mask: fs.PermissionSetting
    other: fs.PermissionSetting
    default_user: fs.PermissionSetting
    default_group: fs.PermissionSetting
    default_mask: fs.PermissionSetting
    default_other: fs.PermissionSetting
    raw_system_output: str=""
    special_users: dict[str, fs.PermissionSetting] = field(
        default_factory=lambda: {})
    special_groups: dict[str, fs.PermissionSetting] = field(
        default_factory=lambda: {})
    default_special_users: dict[str, fs.PermissionSetting] = field(
        default_factory=lambda: {})
    default_special_groups: dict[str, fs.PermissionSetting] = field(
        default_factory=lambda: {})

    @classmethod
    def from_getfacl_cmd_output(cls, cmd_output: str):
        """
        Instantiates a :class: `ACLData` object from Linux getfacl output
        :param cmd_output: Linux getfacl std out
        :return :class: `ACLData` object
        """
        kwargs = {"raw_system_output": cmd_output}
        for item in osp.getfacl_output_items():
            matched_vals = re.findall(
                item.regex, cmd_output, flags=re.MULTILINE
            )
            item.validate_matches(matched_vals)
            kwargs[item.attribute] = item.to_acl_constructor_format(
                matched_vals
            )
        return cls(**kwargs)

    @property
    def effective_permissions(self):
        return EffectivePermissions(self)


class EffectivePermissions:
    def __init__(self, acl_data: ACLData):
        self.user = acl_data.user
        self.special_users = {
                user: fs.compute_effective_permissions(
                    base=permission, mask=acl_data.mask
                )
                for user, permission in acl_data.special_users.items()
            }
        self.group = fs.compute_effective_permissions(
                base=acl_data.group, mask=acl_data.mask
            )

        self.special_groups = {
                user: fs.compute_effective_permissions(
                    base=permission, mask=acl_data.mask
                )
                for user, permission in acl_data.special_groups.items()
            }

        self.other = acl_data.other
        self.default_user = acl_data.default_user
        self.default_special_users = {
                user: fs.compute_effective_permissions(
                    base=permission, mask=acl_data.default_mask
                )
                for user, permission in acl_data.default_special_users.items()
            }

        self.default_group = fs.compute_effective_permissions(
                base=acl_data.default_group, mask=acl_data.default_mask
            )

        self.default_special_groups = {
                group: fs.compute_effective_permissions(
                    base=permission, mask=acl_data.default_mask
                )
                for group, permission in acl_data.default_special_groups.items()
            }

        self.default_other = acl_data.default_other

    def __repr__(self):
        return "\n".join([f"{key}: {val}" for key, val in vars(self).items()])


