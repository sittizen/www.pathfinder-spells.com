import bleach
import html2text
import yaml

from pathfinder_spells.spelltables.models import Mastery, Spell, MASTERY_TYPES, MasteryLevel

remap_spaces = {
    ord('\t'): ' ',
    ord('\f'): ' ',
    ord('\n'): None,
    ord('\r'): None
}


class YamlMastery(yaml.YAMLObject):
    yaml_tag = u'!Mastery'

    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class YamlSpell(yaml.YAMLObject):
    yaml_tag = u'!Spell'

    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.description = html2text.html2text(bleach.clean(self.description, strip=True)).translate(remap_spaces)


def masteries(data):
    for mastery in data['objects']:
        mastery_type = list(MASTERY_TYPES.keys())[list(MASTERY_TYPES.values()).index(mastery.mastery_type)]
        obj, created = Mastery.objects.get_or_create(mastery_type=mastery_type, name=mastery.name)

        for sub_name in getattr(mastery, 'subs', []):
            Mastery.objects.get_or_create(mastery_type=mastery_type, name=sub_name, specializes=obj)


def spells(data):
    for spell in data['objects']:
        obj, created = Spell.objects.get_or_create(name=spell.name)
        obj.components = spell.components
        obj.description = spell.description
        obj.effect = spell.effect
        obj.save()
        for d in spell.domains:
            domain_name, lvl = d.split()
            domain = Mastery.objects.get(name=u"%s Domain" % domain_name, mastery_type=1)
            MasteryLevel.objects.create(level=lvl, spell=obj, mastery=domain)
