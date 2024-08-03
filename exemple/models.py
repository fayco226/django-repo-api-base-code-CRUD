from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Exemple(models.Model):

    

    class Meta:
        verbose_name = _("Exemple")
        verbose_name_plural = _("Exemples")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Exemple_detail", kwargs={"pk": self.pk})