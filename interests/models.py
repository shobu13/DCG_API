from django.db import models


class Interest(models.Model):
    """
    modèle représentant un centre d'interet.
    Si un utilisateur enregistre un interet n'étant pas présent dans la base de donnée, alors on
    le créer.
    """
    name = models.CharField(max_length=30)
