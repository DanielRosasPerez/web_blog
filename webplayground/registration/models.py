from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.urls import reverse

# Para que en la carpeta "media" no se repitan las fotos o elementos que subimos (para este caso, en el campo "avatar" del modelo "Profile"):
def custom_upload_to(instance, filename):
    old_instance = Profile.objects.get(pk=instance.pk)
    old_instance.avatar.delete()
    return "profiles/" + filename

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile_set")
    #avatar = models.ImageField(upload_to="profiles", null=True, blank=True)
    avatar = models.ImageField(upload_to=custom_upload_to, null=True, blank=True) # Igualamos el atributo "upload_to" a la función "custom_upload_to"
    # y de esta forma, evitamos que se almacenen las distintas fotos de perfil que subimos.
    bio = models.TextField(null=True, blank=True)
    link = models.URLField(max_length=200, null=True, blank=True)

    # NOTA: Cuando se intenta almacenar una foto, video, etc. con el mismo nombre que uno que ya se encuentra almacenado, Django en automático
    # agregará un guión bajo y un hash para diferenciarlos en los nombres. Por ejemplo; si una imagen se llama "avatar.png" y la otra que se 
    # intenta guardar tiene el mismo nombre, Django le podría nombrar "avatar_1ZXF.png" (el hash se generá de manera aleatoria, este fue solo
    # un ejemplo). 
    # Para mayor información sobre el atributo "upload_to" ir a: 
    # https://docs.djangoproject.com/en/3.0/ref/models/fields/#django.db.models.FileField.upload_to

    """
    def get_absolute_url(self):
        return reverse("app_profiles:ProfilesDetailView", args=[self.id, self.user])
    """

    class Meta:
        ordering = ["user__username"]

# CREAMOS UNA SEÑAL (signals) para el modelo "Profile":
from django.dispatch import receiver
from django.db.models.signals import post_save
@receiver(post_save, sender=User)
def ensure_profile_exists(sender, instance, **kwargs):
    if kwargs.get("created", False): # Si existe la clave llamada "created" dentro de "kwargs", significa que es la primera vez que se guarda la
        # instancia, por lo tanto, se acaba de crear. De no existir esta entrada en el diccionario, devolveremos "False".
        Profile.objects.get_or_create(user=instance) # Si la instancia se ha creado, crearemos el perfil.
        print("Se acaba de crear un usuario.")