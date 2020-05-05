# -*- coding: utf-8 -*-
"""
Manage the download and untar of the single salt binary
"""
import os
import re
import tarfile

# Import
from distutils.version import LooseVersion

# Import Salt libs
import salt.utils.http
from salt.version import SaltStackVersion

# TODO: Add function that downloads new binary from our hosting location
# when function is added, add new salt-ssh argument that will automatically
# download the latest salt binary from the website


def get_salt_version(pathname=None):
    """
    return salt version from a filename
    """
    fsalt = SaltStackVersion.git_describe_regex
    sver = fsalt.search(pathname)
    if sver:
        sver = sver.group().rstrip(".")
        return sver
    return False


def extract_binary(bin_dir, sver, fpath):
    """
    Create versioned dir and extract tar file into dir
    """
    ver_dir = os.path.join(bin_dir, sver)
    if os.path.exists(ver_dir) and os.path.exists(os.path.join(ver_dir, "salt")):
        # path already exists, and salt already extracted
        return False
    # create version directory
    os.makedirs(ver_dir, exist_ok=True)
    tf = tarfile.open(fpath)
    tf.extractall(path=ver_dir)


def prep_binary(bin_dir, version=None):
    """
    untar all the salt binaries in the directory
    If version is specfiied, only untar for
    that version
    """
    for _file in os.listdir(bin_dir):
        fpath = os.path.join(bin_dir, _file)
        sver = get_salt_version(fpath)
        if sver:
            if version:
                if sver == "salt-" + version:
                    extract_binary(bin_dir, sver, fpath)
            else:
                if os.path.isfile(fpath) and tarfile.is_tarfile(fpath):
                    extract_binary(bin_dir, sver, fpath)


def get_binary_path(bin_dir, latest=True, version=None):
    """
    Return the path to the latest version of the
    salt binary in the bin_dir. This assumes
    the binaries have already been ran through
    prep_binary and have extracted directories.
    """
    latest_ver = ""
    versions = {}
    for _dir in os.listdir(bin_dir):
        fpath = os.path.join(bin_dir, _dir)
        if os.path.isdir(fpath):
            sver = get_salt_version(os.path.basename(_dir))
            if sver:
                sver = sver.replace("salt-", "")
                versions[sver] = fpath
                if not latest_ver:
                    latest_ver = sver
                if LooseVersion(sver) > LooseVersion(latest_ver):
                    latest_ver = sver
    return versions[latest_ver]
