import importlib


def get_class(path):
    [module_path, class_str] = path.split(':')
    module = importlib.import_module(module_path)
    return getattr(module, class_str)
