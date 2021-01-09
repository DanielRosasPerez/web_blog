from django.test import TestCase

# Create your tests here.
from django.contrib.auth.models import User
from .models import Message, Thread

class ThreatTestCase(TestCase):
    
    # NOTA: EL "setUp" SE EJECUTA POR CADA TEST, lo que significa que si deseamos hacer un test con algun elemento creado en un test previo al 
    # que nos encontramos, necesitamos volver a crearlo todo en el nuevo test.

    def setUp(self):
        # Para añadir nuevos usuarios:
        self.user1 = User.objects.create_user("user1", None, "test1234")
        self.user2 = User.objects.create_user("user2", None, "test1234")
        self.user3 = User.objects.create_user("user3", None, "test1234")

        # Para añadir nuevos mensajes:
        self.thread = Thread.objects.create()
    
    def test_add_users_to_thread(self):
        print('\r')
        self.thread.users.add(self.user1, self.user2)
        self.assertEqual(len(self.thread.users.all()),2)

    def test_filter_thread_by_users(self):
        print('\r')
        self.thread.users.add(self.user1, self.user2)
        threads = Thread.objects.filter(users=self.user1).filter(users=self.user2) # Consultar vídeo 86. TDD sección 4.
        self.assertEqual(self.thread, threads[0])

    def test_filter_non_existent_thread(self):
        print('\r')
        threads = Thread.objects.filter(users=self.user1).filter(users=self.user2)
        self.assertEqual(len(threads), 0)


    def test_add_messages_to_thread(self):
        print('\r')
        self.thread.users.add(self.user1, self.user2)
        message_1 = Message.objects.create(user=self.user1, content="Buenas tardes")
        message_2 = Message.objects.create(user=self.user2, content="Muy bien, y usted?")
        self.thread.messages.add(message_1, message_2)
        self.assertEqual(len(self.thread.messages.all()), 2) # Porque hemos agregados 2 mensajes.

        for user, message in zip(self.thread.users.all(), self.thread.messages.all()):
            print(f"User: {user}\nMessage: {message.content}\n")

    def test_add_message_from_user_not_in_thread(self): # Para testear que un usuario no pueda mandar mensajes a un hilo si este no pertenece
        # a él.
        print('\r')
        self.thread.users.add(self.user1, self.user2)
        message_1 = Message.objects.create(user=self.user1, content="Buenas tardes.")
        message_2 = Message.objects.create(user=self.user2, content="Muy bien, y usted?")
        message_3 = Message.objects.create(user=self.user3, content="Las salidas son horneadas.")
        self.thread.messages.add(message_1, message_2, message_3)
        self.assertEqual(len(self.thread.messages.all()), 2)

        for user, message in zip(self.thread.users.all(), self.thread.messages.all()):
            print(f"User: {user}\nMessage: {message.content}\n")

    def test_find_thread_with_custom_manager(self):
        print('\r')
        self.thread.users.add(self.user1, self.user2)
        thread = Thread.objects.find(self.user1,self.user2)
        self.assertEqual(self.thread, thread)

    def test_find_or_create_thread_with_custom_manager(self):
        print('\r')
        self.thread.users.add(self.user1, self.user2)
        thread = Thread.objects.find_or_create(self.user1,self.user2)
        self.assertEqual(self.thread, thread)    
        thread = Thread.objects.find_or_create(self.user1,self.user3)
        self.assertIsNotNone(thread)