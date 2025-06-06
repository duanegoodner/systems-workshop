import subprocess
from abc import ABC, abstractmethod


class SubprocessException(Exception):
    def __init__(self, completed_process: subprocess.CompletedProcess):
        self.completed_process = completed_process

    @property
    @abstractmethod
    def msg(self) -> str:
        return (
            "Subprocess exited abnormally.\n Subprocess args ="
            f" {self.completed_process.args}\n Subprocess return code ="
            f" {self.completed_process.returncode}"
        )

    def __str__(self):
        return self.msg


class GetFaclSubprocessException(SubprocessException):
    @property
    def msg(self) -> str:
        return (
            "\ngetfacl subprocess exited abnormally.\nSubprocess args:"
            f" {self.completed_process.args}\nSubprocess return code:"
            f" {self.completed_process.returncode}"
        )


class ExcessRegexMatches(Exception):
    def __init__(
        self,
        attribute_name: str,
        num_matches_found: int,
        max_allowed_matches: int,
    ):
        self.attribute_name = attribute_name
        self.num_matches_found = num_matches_found
        self.max_allowed_matches = max_allowed_matches

    @property
    def msg(self):
        return (
            f"Regex found {self.num_matches_found} matches for attribute"
            f" {self.attribute_name}.\nMax allowed matches:"
            f" {self.max_allowed_matches}"
        )

    def __str__(self):
        return self.msg


class InsufficientRegexMatches(Exception):
    def __init__(self, attribute_name: str, num_matches_found: int):
        self.attribute_name = attribute_name
        self.num_matches_found = num_matches_found

    @property
    def msg(self):
        return (
            f"Regex found {self.num_matches_found} matches for attribute"
            f" {self.attribute_name}"
        )


class InvalidFileSettingString(Exception):
    def __init__(self, value: any, all_bits_set: str, no_bits_set: str):
        self.value = value
        self.all_bits_set = all_bits_set
        self.no_bits_set = no_bits_set

    @property
    def msg(self):
        return (
            "Invalid value for file setting."
            "Must be a three-character string with:\n"
            f"first character = {self.no_bits_set[0]} or"
            f"{self.all_bits_set[0]}\n"
            f"second character = {self.no_bits_set[1]} or"
            f"{self.all_bits_set[1]}\n"
            f"third character = {self.no_bits_set[2]} or"
            f"{self.all_bits_set[2]}"
        )

    def __str__(self):
        return self.msg


class SpecialPermissionsParsingError(Exception):
    def __init__(self, num_items_parsed: int):
        self.num_items_parsed = num_items_parsed

    @property
    def msg(self):
        return (
            "Expected a key-value pair, but parsed into"
            f" {self.num_items_parsed} items."
        )

    def __str__(self):
        return self.msg
