#from django.contrib.auth.forms import UserCreationForm # Importamos un formulario de autenticación genérico.
from .forms import UserCreationFormWithEmail, ProfileForm, EmailForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.shortcuts import render
from django.http import HttpResponseRedirect

# Create your views here.
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django import forms
class SignUpView(CreateView):
    form_class = UserCreationFormWithEmail # Para no crear un formulario de autenticación, usaremos uno genérico provisto por Django.
    template_name = "registration/signup.html" # En este template renderizamos el formulario.
    
    def post(self, request, *args, **kwargs): # Cuando hagamos click en el botón confirmar del formulario, estaremos realizando una petición
        # "post", y es ahí cuando se activa este método.
        form = self.form_class(request.POST) # Creamos el objeto formulario a partir de los datos ingresados.
        if form.is_valid(): # Verificamos que los datos ingresados al formulario de registro de usuario sean correctos.
            data_register = form.cleaned_data # Extraemos los datos del formulario. Se retorna un diccionario.
            username = data_register["username"] # Extraemos el nombre de usuario.
            password = data_register["password1"] # Extraemos la contraseña.
            email = data_register["email"]
            new_user = User.objects.create_user(username=username, password=password, email=email) # Creamos un nuevo usuario directamente desde el view.
            new_user.save() # Lo guardamos en la base de datos.
            auth_login(request, new_user) # Logeamos al nuevo usuario agregado de manera inmediata.
            return HttpResponseRedirect(reverse_lazy("app_pages:PageListView")) # Regresamos al template "page_list.html".
        else: # En caso de que los datos ingresados no sean validos.
            return render(request, self.template_name, {"form":self.get_form()}) # Renderizamos nuevamente el formulario en el template dado.

        # Para más información sobre la creación de usuarios por medio del shell: 
        # https://stackoverflow.com/questions/18503770/how-to-create-user-from-django-shell
    
    def get_form(self, form_class=None): # Cuando cargamos el template "signup.html", este método es activado.
        form = super(SignUpView, self).get_form() # Recuperamos el formulario y lo guardamos en "form".
        # Modificamos el formulario en tiempo real o de ejecución:
        form.fields["username"].widget = forms.TextInput(attrs={"class":"form-control mb-2", "placeholder":"Nombre de Usuario", "autocomplete":"off"})
        form.fields["email"].widget = forms.EmailInput(attrs={"class":"form-control mb-2", "placeholder":"Email", "autocomplete":"off"})
        form.fields["password1"].widget = forms.PasswordInput(attrs={"class":"form-control mb-2", "placeholder":"Contraseña"})
        form.fields["password2"].widget = forms.PasswordInput(attrs={"class":"form-control mb-2", "placeholder":"Repite la Contraseña"})
        return form

        # NOTA: En el método "get_form()" únicamente estamos sobreescribiendo el "widget". Los campos como tal siguen estando intactos. Si deseamos
        # verificar esto, podemos ir a "forms.py" de esta misma app, y verificar que el campo email esta definido como "EmailField(<atributos>)".
        # Sin embargo, en este método hemos sobreescribido su widget por default dejando intacto la definición original de este campo.

        # Por otro lado, podemos notar que la definición del campo a tráves de "forms" siempre termina en "Input". (forms.TextInput, ..., 
        # forms.PasswordInput).

        # NOTA 2: Modificar los "widgets" en tiempo de ejecución significa que en realidad sólo estamos sobreescribiendo este atributo cuando 
        # mostramos en el template el formulario, por lo que, en realidad. Una vez hacemos click en el botón "Confirmar", se manda una HTTPrequest
        # tipo "POST", la cual recuperamos en el método "post()". Por lo que construimos un objecto del formulario "UserCreationFormWithEmail", el
        # cual (dado que no hemos sobreescribido de manera directa el atributo "widgets"), conserva sus propiedades. Por lo que nos es posible validar
        # los datos. Para más información, consultar la "NOTA 2" del archivo "forms.py" de está app.

    """
    def get_success_url(self): # Una vez damos click en el botón de "Confirmar" (es decir, una vez que rellenamos el formulario y lo
        # enviamos), nos mandará al mismo formulario pero observaremos que en la URL nos aparecerá al final "?register". Esto, con la
        # finalidad de darle retroalimentación al usuario para que sepa que su registro fue éxitoso.

        return reverse_lazy("login") + "?register"
    """

    """
    No hacemos uso de "success_url" debido a que en esta variable no podemos concatenar, como sí se puede en el método "get_succes_url".
    Ambos hacen la misma función.
    """

from django.views.generic.edit import UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.urls import reverse_lazy
@method_decorator(login_required, name="dispatch") # De esta manera, decoramos el método "dispatch" hereado por "View", y nos aseguramos
# de que el usuario se encuentre con la sesión iniciada para poder acceder a la actualización de su perfil. No tiene sentido renderizar el 
# contenido de actualización del perfil de esta vista de manera directa, si el usuario no esta registrado o no ha iniciado sesión. Para tener 
# más clara esta situación, consultar el archivo "views.py" de la app "pages".
class ProfileUpdate(UpdateView):
    # No declaramos "model = ProfileForm" porque ya se encuntra declarado en "ProfileForm".
    form_class = ProfileForm
    template_name = "registration/profile_form.html"
    success_url = reverse_lazy("app_registration:ProfileUpdate")

    def get_object(self): # Para evitar pasar una PRIMARY KEY (pk), o identificar en el "path" (esto, por seguridad; evitamos que alguien que
        # conozca la pk de otro usuario pueda editar su perfil). Para resolver este problema y poder permitirle al usuario que este logueado
        # que pueda editar "su propio perfil", podemos de obtener el "id" del usuario autenticado directamente desde la "request" (aquí se almacena
        # el id), 

        # Recuperamos el objeto que se va a editar:
        profile, create = Profile.objects.get_or_create(user=self.request.user) # Recuperamos o creamos (en caso de que no exista), el user
        # contenido en la misma "request" en tiempo real. Este método devuelve una tupla con dos valores, el perfil y un valor booleano.
        return profile # Returnamos, únicamente el perfil.

        # NOTA: Las "UpdateView" contiene este método llamado "get_object()". Sin embargo, habría que investigar si existe alguna otra "View" que
        # lo contenga.

        # NOTA 2: La "pk" (como en SQL), se le asigna por default al "id" (el cual, en Django, no se tiene que declarar de manera manual).

@method_decorator(login_required, name="dispatch")
class EmailUpdate(UpdateView):
    form_class = EmailForm
    template_name="registration/profile_email_form.html"
    success_url = reverse_lazy("app_registration:ProfileUpdate")

    def get_object(self): # Recuperamos el objecto con el trabajaremos.
        return self.request.user

    def get_form(self, form_class=None):
        form = super(EmailUpdate, self).get_form()
        form.fields["email"].widget = forms.EmailInput(attrs={"class":"form-control mb-2", "placeholder":"Email", "autocomplete":"off"})
        return form