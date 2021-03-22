#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Author:wistn
since:2021-03-11
LastEditors:Do not edit
LastEditTime:2021-03-16
Description:
"""
import os
import re

project_root = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "..")
with open(
    os.path.join(project_root, "pyChakraCore", "CHANGELOG.md"), "r", encoding="utf-8"
) as fs:
    text = fs.read().replace("\r\n", "\n")
regexp = r"(^|\n)(#+\s+\[?v?\d(\.\d){0,2}\]?[\s\S]*?)\n#+ \[?v?\d(\.\d){0,2}\]?"
if re.search(regexp, text, re.I):
    new_section = re.search(regexp, text, re.I)[2]
    """ like:
        ## [2.0.0]
        'second_section'
        # v1
    """
else:
    new_section = re.search(r"(^|\n)(#+\s+\[?v?\d(\.\d){0,2}\]?[\s\S]*)$", text, re.I)[
        2
    ]
    """ like:
        # Changelog
        ### 0.0.1
        'first_section'
    """
version = re.search(r"#+\s+\[?v?(\d(\.\d){0,2})\]?", new_section, re.I)[1]
with open(os.path.join(project_root, "new_section"), "w", encoding="utf-8") as fs:
    fs.write(new_section)
with open(os.path.join(project_root, "version"), "w", encoding="utf-8") as fs:
    fs.write(version)
