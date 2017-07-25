from django.core.validators import validate_comma_separated_integer_list
from django.db import models


MASTERY_TYPES = {
    0: 'School',
    1: 'Domain',
    2: 'Bloodline',
    3: 'Mystery',
    4: 'Patron',
}


class Mastery(models.Model):
    """
    A generic class to represent gerarchy of Schools, Domains, Bloodlines etc.
    """
    mastery_type = models.PositiveIntegerField(choices=MASTERY_TYPES.items(), default=0)
    name = models.CharField(max_length=128)
    specializes = models.ForeignKey('self', null=True, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('mastery_type', 'name', 'specializes')
        ordering = ('mastery_type', 'name')

    # todo checks on save, can't specialize a mastery of different type

    def __str__(self):
        return u"%s: %s" % (MASTERY_TYPES[self.mastery_type],
                            "%s (%s)" % (self.name, self.specializes.name) if self.specializes else self.name)


class PlayerClass(models.Model):
    name = models.CharField(max_length=128, unique=True)
    must_prepare_spells = models.BooleanField(default=True)
    permitted_mastery_types = models.CharField(max_length=16, default='0',
                                               validators=(validate_comma_separated_integer_list, ))

    def __str__(self):
        return u"%s" % self.name

    # todo this class will act as the main facade for queries
    def spell_list(self, mastery_type=0, sub_masteries=[], level=None):

        if mastery_type:
            if not sub_masteries:
                qs = MasteryLevel.objects.filter(mastery__in=Mastery.objects.filter(mastery_type__exact=mastery_type),
                                                 mastery__specializes__isnull=True)
            if sub_masteries:
                qs = MasteryLevel.objects.filter(mastery__in=sub_masteries)
        else:
            if not sub_masteries:
                qs = PlayerClassLevel.objects.filter(player_class__exact=self)
            if sub_masteries:
                qs = PlayerClassLevel.objects.filter(spell__masteries__in=sub_masteries)

        if level is not None:
            qs = qs.filter(level__exact=level)

        return qs.order_by('level', 'spell__name').all()


class Spell(models.Model):
    name = models.CharField(max_length=128, unique=True)
    masteries = models.ManyToManyField(Mastery,
                                       through='MasteryLevel',
                                       through_fields=('spell', 'mastery'))

    def add_to_mastery(self, mastery, level=None):
        MasteryLevel.objects.create(mastery=mastery, spell=self, level=level)
        if mastery.specializes is not None:
            MasteryLevel.objects.create(mastery=mastery.specializes, spell=self, level=level)

    def add_to_playerclass(self, player_class, level=None):
        PlayerClassLevel.objects.create(player_class=player_class, spell=self, level=level)

    # todo custome create method checking that at least a School is associated with spell

    def __str__(self):
        return u"%s\n%s" % (self.name, "".join([" %s\n" % str(ml) for ml in self.masterylevel_set.all()]))


class MasteryLevel(models.Model):
    """
    Generate the list of spelltables by domain|bloodline|etc / level
    """
    level = models.PositiveIntegerField(null=True)  # positioning into School has no level
    spell = models.ForeignKey(Spell, on_delete=models.CASCADE)
    mastery = models.ForeignKey(Mastery, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('level', 'spell', 'mastery')

    def __str__(self):
        return u"%s, lvl %s" % (self.mastery, self.level)


class PlayerClassLevel(models.Model):
    """
    Generate the list of spelltables by class / level
    """
    level = models.PositiveIntegerField()
    spell = models.ForeignKey(Spell, on_delete=models.CASCADE)
    player_class = models.ForeignKey(PlayerClass, on_delete=models.CASCADE)

    def __str__(self):
        return u"%s %s %s" % (self.player_class.name, self.level, self.spell.name)


class SpellsPerDay(models.Model):
    # todo add 'base' to identify common vs specializations ?
    level = models.PositiveIntegerField()
    player_class = models.ForeignKey(PlayerClass)
    mastery_type = models.PositiveIntegerField(default=0)

    num_of_spells = models.PositiveIntegerField()
    apply_attribute_bonus = models.BooleanField(default=True)

    class Meta:
        unique_together = ('level', 'player_class', 'mastery_type')


class SpellsKnown(models.Model):
    level = models.PositiveIntegerField()
    player_class = models.ForeignKey(PlayerClass)
    mastery_type = models.PositiveIntegerField(default=0)
    # todo absence of instance for 'lvl cls mst' axis means there is no cap. put rule in PlayerClass method

    num_of_spells = models.PositiveIntegerField()
    apply_attribute_bonus = models.BooleanField(default=True)

    class Meta:
        unique_together = ('level', 'player_class', 'mastery_type')
