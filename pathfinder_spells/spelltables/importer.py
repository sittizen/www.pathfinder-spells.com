from pathfinder_spells.spelltables.models import Mastery

from pathfinder_spells.spelltables.models import MASTERY_TYPES


def masteries(data):
    mastery_type = list(MASTERY_TYPES.keys())[list(MASTERY_TYPES.values()).index(data['mastery_type'])]
    for slug, mastery_data in data['masteries'].items():
        mastery, created = Mastery.objects.get_or_create(mastery_type=mastery_type, name=mastery_data['name'])
        for sub_name in mastery_data['subs']:
            Mastery.objects.get_or_create(mastery_type=mastery_type, name=sub_name, specializes=mastery)
