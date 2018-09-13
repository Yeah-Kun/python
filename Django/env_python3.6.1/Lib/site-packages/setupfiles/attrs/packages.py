#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

__all__ = ["packages", "package_dir", "package_data"]

cwd = os.getcwd()

# repo/
# repo/packages/
# repo/packages/pkgname1/*.py
# repo/packages/pkgname1/data/*
# repo/packages/pkgname2/*.py
# repo/packages/pkgname2/data/*

# known-issues:
# 1) 'package_dir' used with 'packages' and 'py_modules' (merge required)
# 2) `pip install pkgname` uses tmp folder for generating wheel (setup.py bdist_wheel)
# pip generated files:
#   path/to/tmp/pip-delete-this-directory.txt
#   path/to/tmp/packages/dependency/
#   path/to/tmp/packages/dependency.egg-info/

packages = []
package_data = dict()
package_dir = dict()

path = os.path.join(cwd, "packages")
pip = os.path.join(cwd,"pip-delete-this-directory.txt")

def is_package(path):
    return (
        os.path.isdir(path) and
        os.path.isfile(os.path.join(path, '__init__.py'))
        )

# known-issues: setuptools.find_packages python3.3 nested packages not supported
# fix: user function
def find_packages(path, base="" ):
    """ Find all packages in path """
    packages = {}
    for item in os.listdir(path):
        dir = os.path.join(path, item)
        if is_package( dir ):
            if base:
                module_name = "%(base)s.%(item)s" % vars()
            else:
                module_name = item
            packages[module_name] = dir
            packages.update(find_packages(dir, module_name))
    return packages

if os.path.exists(path) and os.path.isdir(path):
    find = find_packages('packages')
    for package in find.keys():
        path = "packages/%s" % package
        egg_info = "packages/%s.egg-info" % package.split(".")[0]
        if os.path.exists(egg_info) and os.path.exists(pip):
            continue
        packages.append(package)
        # known-issues: package_dir = {'': 'packages'} conflicts with py_modules 
        # fix: don't pack packages and modules in one dist
        package_dir[package] = find[package]
        data = '%s/data' % path
        if os.path.exists(data):
            package_data[package] = ['data/*']


