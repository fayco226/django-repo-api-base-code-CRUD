from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.conf import settings


# Create your models here.

class CommunFieldModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='%(class)s_created'
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='%(class)s_updated'
    )

    class Meta:
        abstract = True

class Exemple(CommunFieldModel):

    name = models.CharField(_(""), max_length=50)
    class Meta:
        verbose_name = _("Exemple")
        verbose_name_plural = _("Exemples")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Exemple_detail", kwargs={"pk": self.pk})
    
class Exemple2(CommunFieldModel):

    name = models.CharField(_(""), max_length=50)
    class Meta:
        verbose_name = _("Exemple")
        verbose_name_plural = _("Exemples")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Exemple_detail", kwargs={"pk": self.pk})