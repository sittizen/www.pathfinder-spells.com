import yaml

from pathfinder_spells.pcs.models import PCClass


class YamlPCClass(yaml.YAMLObject):
    yaml_tag = u'!PCClass'

    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


def pcclass(data):
    for c in data['objects']:
        PCClass.objects.get_or_create(name=c.name)
