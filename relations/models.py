from django.db import models

from main.models import User


class Relation(models.Model):
    """
    Relations between users.

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
        User, related_name='relations', db_index=True)
    to_user = models.ForeignKey(User, db_index=True)
    description = models.CharField(max_length=32, default='')
    opposite = models.IntegerField(default=0, db_index=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    updated = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        unique_together = ('user', 'to_user')
        db_table = 'user_relations'

    @classmethod
    def get_confirmed_relations(cls, from_user):
        return cls.objects.filter(user=from_user,
                                  opposite__gt=0).order_by('-updated')

    @classmethod
    def get_outgoing_relations(cls, from_user):
        return cls.objects.filter(user=from_user,
                                  opposite=0).order_by('-updated')

    @classmethod
    def get_incoming_relations(cls, to_user):
        return cls.objects.filter(to_user=to_user,
                                  opposite=-1).order_by('-updated')

    def get_opposite(self):
        """
        Get the opposite relation.

        Set opposite equal 0, if current relation is outgoing relation.
        Set opposite equal -1, if current relation is incoming relation.
        """
        try:
            return Relation.objects.get(user_id=self.to_user,
                                        to_user_id=self.user)
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
        outgoing = self.get_opposite(0)
        if outgoing is not None:
            outgoing.opposite = self.id
            self.opposite = outgoing.id
            outgoing.save()
            self.save()

    def deny(self):
        """
        Deny an incoming relation.
        """
        outgoing = self.get_opposite(0)
        if outgoing is not None:
            outgoing.delete()
        self.delete()
