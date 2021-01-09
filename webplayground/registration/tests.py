from django.test import TestCase

# Create your tests here.
from .models import Profile
from django.contrib.auth.models import User

class ProfileTestCase(TestCase):
    def setUp(self): # Este es el primer método que se debe declarar. Es un must.
        User.objects.create_user("test", "test@test.com", "test1234") # Se creará este usuario de pruebas.

    # Esto se ejecutará después de que se cree el usuario:
    def test_profile_exists(self): # Configuramos la prueba en sí. La prueba puede llamarse como sea, pero debe comenzar con "test_".
        exists = Profile.objects.filter(user__username="test").exists() # Devolverá "True" o "False".
        self.assertEqual(exists, True) # Para comprobar que exists tenga el valor "True".

    # CONCLUSIÓN: En el primer método se generá la instancia a la cual realizarle la prueba. En el segundo método añadimos el código que será
    # para realizar la prueba.

# NOTA: EL "setUp" SE EJECUTA POR CADA TEST, lo que significa que si deseamos hacer un test con algun elemento creado en un test previo al que nos
# encontramos, necesitamos volver a crearlo todo en el nuevo test.