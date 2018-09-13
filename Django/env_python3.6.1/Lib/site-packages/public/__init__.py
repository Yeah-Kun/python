#!/usr/bin/env python
import copy
import inspect
import os
import sys


def caller_modules():
    try:
        frames = inspect.getouterframes(inspect.currentframe())
        _caller_modules = []
        # frame,filename,line_number,function_name,lines,index
        for frame, _, _, _, _, _ in frames:
            module = inspect.getmodule(frame)
            if module and module not in _caller_modules:
                _caller_modules.append(module)
        return _caller_modules
    except IndexError:
        return []


def append(module, name):
    __all__ = module.__dict__.setdefault('__all__', [])
    if name not in __all__:  # Prevent duplicates if run from an IDE.
        __all__.append(name)
        # if debug:
        # print("%s.__all__ +%s" % (module.__name__,name))
        setattr(module, "__all__", sorted(__all__))


def isstring(value):
    try:
        int(value)
        return False
    except ValueError:
        return True
    except Exception:
        return False


def equal_id(obj1, obj2):
    return id(obj1) == id(obj2)


def validate_module(module):
    if module is None:
        err = "module is None"
        raise Exception(err)
    if not hasattr(module, "__file__"):
        # system module?
        err = "%s has no attribute __file__" % module
        raise Exception(err)


def ispackage(module):
    path = module.__file__
    return "__init__.py" in os.path.basename(path)


def publish_string2module(name, module, force=False):
    path = module.__file__
    dirname = os.path.dirname(path)
    if not hasattr(module, name) and not force:
        # not object name or not exists
        # object str value?
        for mname, member in inspect.getmembers(module):
            if equal_id(member, name):
                return publish2module(mname, module)
    append(module, name)
    if not ispackage(module):  # module
        # find parent package
        # iterate sys.modules
        for _, m in copy.copy(sys.modules).items():
            if not m or not hasattr(m, "__file__"):
                continue
            if ispackage(m) and os.path.dirname(m.__file__) == dirname:
                publish2module(name, m)


def publish_object2module(obj, module):
    name = obj.__name__
    return publish2module(name, module, force=True)


def find_object(obj, module):
    for _, member in inspect.getmembers(module):
        if equal_id(member, obj):
            return member
    for _, member in inspect.getmembers(module):
        if member == obj:
            return member


def publish2module(obj, module, force=False):
    validate_module(module)
    path = module.__file__
    if isstring(obj):  # string
        name = obj
        return publish_string2module(name, module, force)
    if inspect.isclass(obj) or inspect.isroutine(obj):
        name = obj.__name__
        return publish_string2module(name, module, force=True)
    # find object, compare by id
    find = find_object(obj, module)
    if find is not None:
        publish2module(find, module)
    # fix imp.load_module with custom name
    # search same module
    for _, m in sys.modules.items():
        if m and hasattr(m, "__file__") and m.__file__ == path:
            find = find_object(obj, m)
            if find is not None:
                publish2module(find, m)
    # find object last try
    # for mname,member in inspect.getmembers(module):
        # if member==object:
            # return publish2module(mname,module)
    err = "%s not exists in %s" % (obj, module)
    raise Exception(err)


def result(objects):
    if len(objects) == 1:
        return objects[0]
    else:
        return objects


def validate_type(obj):
    if not (inspect.isclass(obj) or inspect.isfunction(obj) or isstring(obj)):
        err = "@public expected class, function or str object name"
        raise TypeError(err)


def public(*objects):
    """public decorator for __all__
    """
    modules = caller_modules()
    if len(modules) == 1 or (objects and objects[0] == public):
        module = modules[0]
    else:
        modules = modules[1:]  # exclude public
        module = modules[0]
    if not module:  # error?
        return result(objects)
    for _object in objects:
        if not hasattr(_object, "__name__"):
            for k, v in module.__dict__.items():
                if v == _object:
                    _object = k
        validate_type(_object)
        modnames = module.__name__.split(".")
        for i, _ in enumerate(modnames):
            fullname = ".".join(modnames[0:i + 1])
            if fullname in sys.modules:
                module = sys.modules[fullname]
                publish2module(_object, module)
    return result(objects)

public(public)
