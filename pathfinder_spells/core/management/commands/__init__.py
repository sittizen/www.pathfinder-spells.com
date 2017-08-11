import yaml

from pathfinder_spells.pcs.importer import YamlPCClass
from pathfinder_spells.spelltables.importer import YamlMastery, YamlSpell


def spell_constructor(loader, node):
    return YamlSpell(**loader.construct_mapping(node))
yaml.add_constructor(u'!Spell', spell_constructor)


def mastery_constructor(loader, node):
    return YamlMastery(**loader.construct_mapping(node))
yaml.add_constructor(u'!Mastery', mastery_constructor)


def pcclass_cosntructor(loader, node):
    return YamlPCClass(**loader.construct_mapping(node))
yaml.add_constructor(u'!PCClass', pcclass_cosntructor)
