from django.core.validators import validate_comma_separated_integer_list
from django.db import models


MASTERIES_TYPES = {
    1: 'Domain',
    2: 'School',
    3: 'Bloodline',
}


class Mastery(models.Model):
    spell_type = models.PositiveIntegerField(choices=MASTERIES_TYPES.items())
    name = models.CharField(max_length=128)
    specializes = models.ForeignKey('self', null=True, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('spell_type', 'name')

    def __str__(self):
        return u"%s: %s" % (MASTERIES_TYPES[self.spell_type],
                            "%s (%s)" % (self.name, self.specializes.name) if self.specializes else self.name)


class PlayerClass(models.Model):
    name = models.CharField(max_length=128, unique=True)
    permitted_masteries_types = models.CharField(max_length=16, validators=(validate_comma_separated_integer_list, ))
    masteries = models.ManyToManyField(Mastery)

    def __str__(self):
        return u"%s" % self.name


class Spell(models.Model):
    name = models.CharField(max_length=128, unique=True)
    masteries = models.ManyToManyField(Mastery,
                                       through='MasteryLevel',
                                       through_fields=('spell', 'mastery'))

    def add_to_mastery(self, mastery, level):
        MasteryLevel.objects.create(mastery=mastery, spell=self, level=level)

    def __str__(self):
        return u"%s\n%s" % (self.name, "".join([" %s\n" % str(ml) for ml in self.masterylevel_set.all()]))


class MasteryLevel(models.Model):
    level = models.PositiveIntegerField()
    spell = models.ForeignKey(Spell, on_delete=models.CASCADE)
    mastery = models.ForeignKey(Mastery, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('level', 'spell', 'mastery')

    def __str__(self):
        return u"%s, lvl %s" % (self.mastery, self.level)


class SpellsPerDay(models.Model):
    level = models.PositiveIntegerField()
    num_of_spells = models.PositiveIntegerField()
    player_class = models.ForeignKey(PlayerClass)

    class Meta:
        unique_together = ('level', 'num_of_spells', 'player_class')
