from model.core import Core
from model.image import Image


def all_subclasses(cls: type):
    classes = []
    for cla in cls.__subclasses__():
        classes.append(cla)
        classes.extend(all_subclasses(cla))
    return classes
