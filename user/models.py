from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.password_validation import validate_password


class User(AbstractUser):
    """
    Ce modèle est une extention du modèle user de base, il rajoute plusieurs champs.
    act_prop_tous : ce champs définis si un utilisateur souhaite voir les activitées proposée
    par tout le monde.

    act_part_visible : ce champs définis si l'utilisateur veut que sa participation à une activité
    sois visible par ses amis.

    act_part_tous : ce champs définis si l'utilisateur veut que sa participation à une activité
    sois visible par ses amis ET par tous, ce champs ne devrait prendre effet que si le précédent
    à été mit à True.
    """
    street = models.TextField()
    city = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=5, default='')
    phone_number = models.CharField(max_length=12)
    birth_date = models.DateField(null=True)
    photo = models.ImageField(upload_to='users/photos/', blank=True)
    # Confidentialité
    act_prop_tous = models.BooleanField(default=False)
    act_part_visible = models.BooleanField(default=False)
    act_part_tous = models.BooleanField(default=False)
    # Social
    # TODO créer les tables et gérer les clé étrangères.
    # lieux_fav = clé étrangère vers table lieux, utile pour faire des comparaison entre users
    # centres_interets = de même
    amis = models.ManyToManyField('User', blank=True)
    est_verif = models.BooleanField(default=False)
    # bloque = clé étrangère vers une table "bloquage"
    stay_connected = models.BooleanField(default=False)
    # signalement = clé étrangère vers table signalement

    def save(self, *args, **kwargs):
        """surcharge de la méthode save de la class Model qui s'exécute à la sauvegarde d'un objet,
        on y ajoute ici un validator permettant de valider le mot de passe entré."""
        if not self.pk:
            validate_password(self.password)
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return "{} {}".format(self.last_name, self.first_name)
