from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from .models import Thread, Message
# Recuperamos los decoradores a usar:
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404, JsonResponse
from django.contrib.auth.models import User
from django.urls import reverse_lazy

@method_decorator(login_required, name="dispatch") # Nos aseguramos que el usuario se encuentra logueado.
class ThreadList(TemplateView):
    template_name="messenger/thread_list.html"

    # Recordemos que podemos hacer uso de la relación inversa en "Thread" con "user_instance.threads.all()" para recuperar todos los hilos o
    # conversaciones de los que forma parte dicho usuario. Por lo tanto, directamente en este template podemos consultar todos los hilos del
    # usuario.

@method_decorator(login_required, name="dispatch") # Nos aseguramos que el usuario se encuentra logueado.
class ThreadDetailView(DetailView):
    model = Thread

    def get_object(self): # Esté método es propio de las "DetailView" ya que sólo se trata de un objeto a mostrar.
        obj = super(ThreadDetailView, self).get_object() # Recuperamos el objeto a mostrar.
        if self.request.user not in obj.users.all(): # De esta forma, nos aseguramos de que el usuario esta accediendo a un hilo del cual SÍ
            # forma parte. De lo contrario, no podrá accesar a dicha conversación o hilo. Con "obj.users.all()" obtenemos los usuarios que
            # pertenecen a dicho hilo.
            raise Http404 # Si no forma parte de la conversación arrojamos un error.
        else: # Siempre y cuando el usuario forme parte de la conversación regresamos el hilo.
            return obj

def add_message(request, pk):
    json_response = {'created':False}
    if request.user.is_authenticated:
        content = request.GET.get('content', None)
        if content:
            thread = get_object_or_404(Thread, pk=pk) # Recuperamos o creamos el objecto conversación/hilo.
            message = Message.objects.create(user=request.user, content=content) # Creamos un mensaje con el contenido y usuario respectivo.
            thread.messages.add(message) # Agregamos el mensaje.
            json_response['created'] = True # Y finalmente, cambiamos el valor del diccionario a True. Así, notificamos la creación del mensaje.
            if len(thread.messages.all()) is 1:
                json_response['first'] = True
    else:
        raise Http404("User is not authenticated")

    return JsonResponse(json_response)

@login_required
def start_thread(request, username):
    user = get_object_or_404(User, username=username)
    thread = Thread.objects.find_or_create(user, request.user)
    return redirect(reverse_lazy('app_messenger:ThreadDetailView', args=[thread.pk]))