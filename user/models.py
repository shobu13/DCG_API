from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.password_validation import validate_password


class User(AbstractUser):
    street = models.TextField()
    city = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=5, default='')
    phone_number = models.CharField(max_length=12)
    birth_date = models.DateField(null=True)
    photo = models.ImageField(upload_to='users/photos/')
    # confidentialité
    act_prop_tous = models.BooleanField(default=False)
    act_part_visible = models.BooleanField(default=False)
    act_part_tous = models.BooleanField(default=False)
    # lieux_fav =
    # centres_interets =
    # act_fav =
    # amis =
    # bloque =
    stay_connected = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        """surcharge de la méthode save de la class Model qui s'exécute à la sauvegarde d'un objet,
        on y ajoute ici un validator permettant de valider le mot de passe entré."""
        if not self.pk:
            validate_password(self.password)
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return "{} {}".format(self.last_name, self.first_name)
