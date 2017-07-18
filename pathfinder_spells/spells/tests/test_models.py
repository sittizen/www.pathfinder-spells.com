from test_plus.test import TestCase

from pathfinder_spells.spells.models import (PlayerClass, Mastery, Spell, SpellsPerDay)


class TestSpells(TestCase):
    def test_bard(self):
        pass

    def test_cleric(self):
        cleric = PlayerClass.objects.create(name='Cleric', permitted_mastery_types='0,1')

        conjuration_school = Mastery.objects.create(name='Conjuration')
        summoning_school = Mastery.objects.create(name='Summoning', specializes=conjuration_school)

        air_domain = Mastery.objects.create(mastery_type=1, name='Air')
        cloud_subdomain = Mastery.objects.create(mastery_type=1, name='Cloud', specializes=air_domain)

        water_domain = Mastery.objects.create(mastery_type=1, name='Water')

        obscuring_mist = Spell.objects.create(name='Obscuring Mist')
        obscuring_mist.add_to_mastery(conjuration_school)
        obscuring_mist.add_to_mastery(air_domain, 1)
        obscuring_mist.add_to_mastery(water_domain, 1)
        obscuring_mist.add_to_playerclass(cleric, 1)

        solid_fog = Spell.objects.create(name='Solid Fog')
        solid_fog.add_to_mastery(conjuration_school)
        solid_fog.add_to_mastery(cloud_subdomain, 4)

        abundant_ammunition = Spell.objects.create(name='Abundant Ammunition')
        abundant_ammunition.add_to_mastery(summoning_school)
        abundant_ammunition.add_to_playerclass(cleric, 1)

        print(cleric.spell_list())
        print(cleric.spell_list(0, [conjuration_school, ]))

        print(cleric.spell_list(1))
        print(cleric.spell_list(1, [water_domain, ]))
        print(cleric.spell_list(1, [], 4))

        print(cleric.spell_list(2))
