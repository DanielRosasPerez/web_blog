from django.db import models
from ckeditor.fields import RichTextField
from django.urls import reverse

class Page(models.Model):
    title = models.CharField(verbose_name="Título", max_length=200)
    content = RichTextField(verbose_name="Contenido")
    order = models.SmallIntegerField(verbose_name="Orden", default=0)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    class Meta:
        verbose_name = "página"
        verbose_name_plural = "páginas"
        ordering = ['order', 'title']

    def __str__(self): # This way, when we are at admin we are going to see the "title" as the name of the instance, instead the name
        # that Django gives to the object.
        return self.title

    def get_absolute_url(self):
        #return reverse("app_pages:page", args=[self.id, self.title])
        return reverse("app_pages:PageDetailView", args=[self.id, self.title])

    # Note: Django will create the URL using the "get_absolute_url" from the model. That's why, sometimes when we are editing some forms or
    # or stuff like that we are going to be sent once we have finshed (in this particular case), to "PageDetailView", unless we specify the
    # opposite inside our respective view from "views.py".
