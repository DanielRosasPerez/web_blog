from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Message(models.Model): # Para crear los mensajes.
    user = models.ForeignKey(User, on_delete=models.CASCADE) # De esta forma, si se borra el usuario, también se elimina la instancia.
    content = models.TextField() # Aquí irá el contenido del mensaje.
    created = models.DateTimeField(auto_now_add=True) # Registramos la fecha de creación del mensaje.

    class Meta:
        ordering = ["created"] # En este caso, conviene ordernar los mensajes del más antiguo al más moderno. Como en cualquier app de mensajería.

class ThreadManager(models.Manager):
    def find(self, user1, user2): # Para encontrar a los usuarios.
        queryset = self.filter(users=user1).filter(users=user2)
        if len(queryset) > 0:
            return queryset[0] # De esta forma devolvemos el hilo en la primera posición. Suponiendo que no tendremos más de 1.
        return None

    def find_or_create(self, user1, user2): # Para encontrar el hilo de conversación existente entre dos usuarios o crearlo.
        thread = self.find(user1, user2)
        if thread is None:
            thread = Thread.objects.create()
            thread.users.add(user1, user2)
        return thread

class Thread(models.Model):
    users = models.ManyToManyField(User, related_name="threads") # Para por medio de una relación inversa, accedemos a todos los hilos a los que
    # pertenece la instancia User correspondiente. Esto se hace con "User_instancia.threads.all()".
    messages = models.ManyToManyField(Message) # Almacenamos todos los mensajes que forman parte del Hilo (o instancia del modelo "Thread").
    updated = models.DateTimeField(auto_now=True)

    objects = ThreadManager() # Sobrescribimos el manager por default.

    class Meta:
        ordering = ["-updated"]

# CREAMOS UNA SEÑAL:
from django.db.models.signals import m2m_changed

def messages_changed(sender, **kwargs):
    instance = kwargs.pop("instance", None)
    action = kwargs.pop("action", None)
    pk_set = kwargs.pop("pk_set", None)
    print(instance, action, pk_set)

    false_pk_set = set()
    if action is "pre_add":
        for msg_pk in pk_set:
            msg = Message.objects.get(pk=msg_pk)
            if msg.user not in instance.users.all():
                print(f"Ups, ({msg.user}) no forma parte del hilo.")
                false_pk_set.add(msg_pk)
    
    # Buscamos los mensajes de "false_pk_set" que SÍ están en "pk_set" y los borramos de "pk_set":
    pk_set.difference_update(false_pk_set)

    # Forzamos la actualización de los chats con los distintos usuarios en el template "thread_list.html":
    instance.save()

    # Hemos conseguido validar un test (test_add_message_from_user_not_in_thread), sin alterarlo haciendo use de esta señal.

m2m_changed.connect(messages_changed, sender=Thread.messages.through)

# PARA MAYOR INFORMACIÓN SOBRE "m2m_changed" consultar: https://docs.djangoproject.com/en/3.1/ref/signals/#m2m-changed