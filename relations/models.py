from django.conf import settings
from django.db import models

USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class Relation(models.Model):
    """
    User Relation model.

    user: An object of user who cares another user.
    to_user: An object of user who is cared by another user.
    description: A user defined description for the relation.
    opposite: The opposite relation's id.
        If it is 0, it is an outgoing relation.
        If it is -1, it is an incoming relation.
    created: Created time.
    updated: Last modified time.
    """
    user = models.ForeignKey(
        USER_MODEL, related_name='relations', db_index=True)
    to_user = models.ForeignKey(USER_MODEL, db_index=True)
    description = models.CharField(max_length=32, default='', blank=True)
    opposite = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    updated = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        unique_together = ('user', 'to_user')
        db_table = 'user_relations'

    @classmethod
    def build_relations(cls, from_user, to_user):
        """
        """
        r1, _ = cls.objects.get_or_create(user=from_user, to_user=to_user)
        r2, _ = cls.objects.get_or_create(user=to_user, to_user=from_user,
                                          opposite=r1.pk)
        r1.opposite = r2.pk
        r1.save()

    def get_opposite(self):
        """
        Get the opposite relation.

        Set opposite equal 0, if current relation is outgoing relation.
        Set opposite equal -1, if current relation is incoming relation.
        """
        try:
            return Relation.objects.get(user=self.to_user, to_user=self.user)
        except Relation.DoesNotExist:
            return None

    def destroy(self):
        """
        Destroy the relation and its opposite relation.
        """
        opposite = self.get_opposite()
        if opposite is not None:
            opposite.delete()
        self.delete()

    def allow(self):
        """
        Allow an incoming relation.
        """
        outgoing = self.get_opposite()
        if outgoing is not None:
            outgoing.opposite = self.id
            self.opposite = outgoing.id
            outgoing.save()
            self.save()

    def deny(self):
        """
        Deny an incoming relation.
        """
        outgoing = self.get_opposite()
        if outgoing is not None:
            outgoing.delete()
        self.delete()
