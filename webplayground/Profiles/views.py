from django.shortcuts import render

# Create your views here.
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from registration.models import Profile
from django.shortcuts import get_object_or_404

class ProfilesListView(ListView):
    model = Profile
    context_object_name = "profiles"
    template_name = "Profiles/profile_list.html"
    paginate_by = 3 # Declaramos el número de instancias que apareceran por página.

class ProfilesDetailView(DetailView):
    model = Profile
    context_object_name = "profile"
    template_name = "Profiles/profile_detail.html"

    def get_object(self): # Recuperamos el objeto para mostrar. En caso de que no exista, se muestra el error "404".
        return get_object_or_404(Profile, user__username=self.kwargs["username"]) # Pasamos el argumento "username" de la url para filtrar el
        # objecto que deseamos.

    # NOTA: Cuando estemos usando una "DetailView", por default, se nos pide que para recuperar la vista del objeto deseado debemos de pasar
    # en la URL la Primary Key (pk, la cual siempre corresponde al "id"), o un campo slug (en caso de que hayamos declarado uno en el modelo).
    # Sin embargo, si no deseamos pasar ninguno de estos argumentos para recuperar la vista detallada del objeto deseado, podemos implementar
    # lo que se realizo en esta app:

    # 1. Hacer uso del template tag {% url '<app_name:name>' object.attribute %}
    # 2. Agregar en "urls.py" en el path el espacio para "object.attribute". De esta forma lo pasaremos a "views.py".
    # 3. En "views.py" agregar el método "get_object(self)", para recuperar el objeto/instancia deseada.

    # Ejemplo:
    # 1. En "profile_list.html" puse lo siguiente {% url 'app_profiles:ProfilesDetailView' profile.user %} como enlace en el nombre del usuario.
    # 2. En "urls.py" dentro de "urlspatterns = []" agregue "path('<username>/', ProfilesDetailView.as_view(), name="ProfilesDetailView")".
    # 3. Una vez en "views.py", en la CBV "ProfilesDetailView" en el método "get_object()" recuperamos el objecto por medio del "username".

    # En este ejemplo se sigue la secuencia del 1 al 3 necesaria para recuperar el objecto deseado. En este caso al Usuario.
