from test_plus.test import TestCase

from pathfinder_spells.spells.models import (PlayerClass, Mastery, Spell, MasteryLevel, SpellsPerDay)


class TestSpells(TestCase):

    def setUp(self):
        pass

    def test_use(self):
        air_domain = Mastery.objects.create(spell_type=1, name='Air')
        water_domain = Mastery.objects.create(spell_type=1, name='Water')
        cloud_subdomain = Mastery.objects.create(spell_type=1, name='Cloud', specializes=air_domain)

        obscuring_mist = Spell.objects.create(name='Obscuring Mist')
        obscuring_mist.add_to_mastery(air_domain, 1)
        obscuring_mist.add_to_mastery(water_domain, 1)
        print(obscuring_mist)

        solid_fog = Spell.objects.create(name='Solid Fog')
        solid_fog.add_to_mastery(cloud_subdomain, 4)
        print(solid_fog)

        cleric = PlayerClass.objects.create(name='Cleric', permitted_masteries_types='1')

        cleric.masteries.add(air_domain)
        cleric.masteries.add(water_domain)
        cleric.masteries.add(cloud_subdomain)
