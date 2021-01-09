from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from .models import Page
from .forms import PageForm # Importamos el formulario creado a partir de los campos del modelo Page.

# CRUD: Create (CreateView), Read (ListViews, DetailView), Update (UpdateView) and Delete (DeleteView).

# MIXINS:

class StaffRequiredMixin():
    """
    Este "mixin" requerirá que el usuario sea miembro del staff.
    """

    def dispatch(self, request, *args, **kwargs): # El despachador de URLs de Django.
        if not request.user.is_staff: # En caso de que el usario intente crear, actualizar o borrar una página y no se encuentre registrado,
            # lo redireccionaremos al login del admin para que inicie sesión.
            return redirect(reverse_lazy("admin:login"))
        return super(StaffRequiredMixin, self).dispatch(request, *args, **kwargs) # En caso de que ya se encuentre registrado y sea "staff", 
        # le será posible realizar las operaciones CRUD.

        """
        Este método controla la petición. Es decir, cuando damos click en cualquier botón de nuestra página web hacemos una solicitud 
        HTTP request. Para este caso, cuando realizamos la solicitud, al controlar la petición de origen podemos dar o no acceso a un usuario
        si es que este esta registrado y además es "staff". De otro forma, no tendrá acceso a las operaciones CRUD y se le pedirá que se registre.
        """

# Nota: Un Mixin es una implementación de una o varias funcionalidades para una clase. Se crea el mixin (una clase), y heredamos su comportamiento
# (es decir, su código), en donde se requiera dando prioridad a su implementación antes que al código de la clase hijo.

# Para este caso, se crea el Mixin (la clase), y posteriormente se herede de él a las vistas. El Mixin tendrá prioridad de ejecución sobre el 
# código propio de cada vista. Esto, para evitar repetir código en común dentro de las vistas.
# En conclusión, un Mixin sería el equivalente al template en común creado para cargar los datos desde ahí, en lugar de estar poniendolos 
# explicítamente en cada template, recordemos que usamos {% include 'path' %} para incluir el código dentro del template "pages_menu.html",
# el cuál contiene los datos en común que todos los templates dentro del directorio "templates/pages" tienen en común.

# Nota 2: AL HEREDERAR EL MIXIN EN UNA VISTA, ESTE, "SIEMPRE DEBE SER EL PRIMER ARGUMENTO". Esto se aprecia en las vistas "Create, Update y 
# Delete".

# DECORADORES PARA LA IDENTIFICACIÓN DE USUARIOS:
"""
Django incluye varias funciones decoradoras para requerir la identificación del usuario antes de devolver una vista.

Por lo tanto, en lugar de hacer uso del código dentro del Mixin previo, podemos hacer uso de decoradores de identificación 
para que quede de la siguiente manera:

################################################################################################

from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator

class StaffRequiredMixin():

    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super(StaffRequiredMixin, self).dispatch(request, *args, **kwargs)

################################################################################################

NOTA:   A diferencia de un decorador tradicional para una función o un método dentro de una clase; en un Mixin, no podemos declararlos de
        de manera directa sobre la función, debemos hacer uso de "@method_decorator(<decorator>)". Esto, se aprecia en el Mixin previo.

NOTA 2: Cuando hacemos uso de decoradores NO ESTAMOS OBLIGADOS A USAR MIXINS, sino que podemos declararlos de manera directa en las vistas.
        Esto, se aprecia a continuación:

################################################################################################

@method_decorator(staff_member_required, name="dispatch") # Debemos indicar que método queremos decorar, para esto usamos el atributo "name".
class PageCreate(CreateView):
    model = Page
    form_class = PageForm
    success_url = reverse_lazy("app_pages:PageListView")

@method_decorator(staff_member_required, name="dispatch")
class PageListView(ListView):
    model = Page
    context_object_name = "pages"

@method_decorator(staff_member_required, name="dispatch")
class PageDetailView(DetailView):
    model = Page
    contex_object_name = "page"

@method_decorator(staff_member_required, name="dispatch")
class PageUpdate(UpdateView):
    model = Page
    context_object_name = "page"
    form_class = PageForm

    def get_success_url(self):
        return reverse_lazy("app_pages:PageUpdate", args=[self.object.id, self.object.title]) + '?ok'

@method_decorator(staff_member_required, name="dispatch")
class PageDelete(DeleteView):
    model = Page
    context_object_name = "page"
    template_name_suffix = "_confirm_delete"
    success_url = reverse_lazy("app_pages:PageListView")

################################################################################################

NOTA:   Dado que todas estas vistas (CreateView, ListView, DetailView, UpdateView, DeleteView), tiene en común al método "dispatch" (el cual 
        es propio de la clase "View" --clase de la cual heredan las vistas CRUD--), debemos especificar (para este caso), que este método es el
        queremos decorar.

EXISTEN OTRAS FUNCIONES DECORADORAS COMO:

a)  login_required

    Este decorador sirve para comprobar que un usuario esta identificado (sin necesidad de que sea miembro del "staff", etc).
    Se importa de: "from django.contrib.auth.decorators import login_required".

b)  permission_required

    Para verificar que un usuario esta identificado y que a la vez tenga un permiso en concreto.

Ambas funciones se importan de la misma dirección que "staff_member_required":
from django.contrib.admin.views.decorators import ...

De igual manera, demeos usar "@method_decorator(<decorator>)" para hacer uso de dichos decoradores.

    PARA MAYOR INFORMACIÓN SOBRE ESTOS DECORADORES, ENTRE OTROS:
    https://docs.djangoproject.com/en/3.1/topics/auth/default/

    PARA MAYOR INFORMACIÓN DE COMO DECORAR LAS "CBV":
    https://docs.djangoproject.com/en/3.1/topics/class-based-views/intro/
    
"""

# Create your views here.

# Forma actual de crear las distitas "views":

class PageListView(ListView):
    model = Page # Esta vista gestionará el modelo "Page". Recuperamos todas las instancias creadas a partir del modelo Page.
    context_object_name = "pages" # El valor por default para la CBV que hereda de "ListView" es: "object_list". Aunque también 
    # podemos hacer uso del nombre modelo en minúsculas + _list; para este caso: "page_list".

    # Por default, el template en donde se nos manda el diccionario de contexto (con los campos propios de cada modelo), se compone por:
    # "nombre del modelo en minúsculas"_"list".html
    # Para este caso, este template a crear se debe llamar: "page_list.html".
    # Podemos modificar este comportamiento al declarar el atributo: "template_name = <nombre_template>.html".


# FBV:
"""
def pages(request):
    pages = get_list_or_404(Page)
    return render(request, 'pages/page_list.html', {'pages':pages})
"""

class PageDetailView(DetailView):
    model = Page # Esta vista gestionará el modelo "Page". Recuperamos todas las instancias creadas a partir del modelo Page.
    context_object_name="page" # El valor por default para la CBV que hereda de "DetailView" es: "object". Aunque también podemos
    # hacer uso del nombre del modelo en minúsculas; para este caso: "page".

    # Por default, el template en donde se nos manda el diccionario de contexto (con los campos propios de cada model), se compone por:
    # "nombre del modelo en minúsculas_detail.html"
    # Para esta CBV, el template a crear para renderizar se debe llamar: "page_detail.html".
    # Podemos modificar este comportamiento al declarar el atributo: "template_name = <nombre_template>.html".

# FBV:
"""
def page(request, page_id, page_title):
    page = get_object_or_404(Page, id=page_id)
    return render(request, 'pages/page_detail.html', {'page':page})
"""

class PageCreate(StaffRequiredMixin, CreateView):
    model = Page # Recuperamos todas las instancias creadas a partir del modelo Page.
    form_class = PageForm # Dado que en el formulario "PageForm" ya hemos indicado los campos del mismo, no es necesario incluir la siguiente lína
    # de código (fields), por esa razón esta comentada.

    #fields=["title", "content", "order"] # Desplegamos en el formulario los capos del modelo "Page" necesarios para la creación de una instancia.

    # Se nos crea un "form genérico" con los campos indicados en "fields". Sin embargo, para este caso, ya hemos creado un formulario llamado
    # "PageForm".

    # Por default, el template en donde se renderiza el formulario se compone de "<nombre del modelo en minúsculas>_form.html". Para este caso,
    # el template a crear dentro de "templates/pages" se debe llamar: "page_form.html".
    # Como ya sabemos, para esta CBV si deseamos renderizar en otro template o cambiar el nombre del template a crear, debemos especificar el
    # atributo "template_name = <nombre del template>.html".

    success_url = reverse_lazy("app_pages:PageListView") # De esta manera, una vez demos click en el botón <input> del formulario creado en el 
    # template "page_form.html" para crear una nueva instancia del modelo "Page", nos redireccionará a "PageListView".

class PageUpdate(StaffRequiredMixin, UpdateView):
    model = Page # Recuperamos todas las instancias creadas a partir del modelo Page.
    context_object_name = "page"
    form_class = PageForm
    #fields = ["title", "content", "order"] # Dado que "fields" ya se encuentra definido en el formulario "PageForm" se comenta. Más info en
    # la vista "PageCreate".
    template_name_suffix = "_update_form" # "pages/page_update_form.html" -> "pages/<nombre del modelo en minúsculas>_update_form.html"

    def get_success_url(self): # Una vez dando click en el botón del formulario "page_update_form.html", seremos redireccionados a la URL formada
        # por reverse_lazy() + '?ok'.
        return reverse_lazy("app_pages:PageUpdate", args=[self.object.id, self.object.title]) + '?ok'

        """
        Este método se encarga de gestionar la petición GET. Y controla la respuesta.
        """
        
class PageDelete(StaffRequiredMixin, DeleteView): # Borramos la página deseada.
    model = Page # Recuperamos todas las instancias creadas a partir del modelo Page.
    context_object_name = "page"
    template_name_suffix = "_confirm_delete" # "pages/page_confirm_delete.html".
    success_url = reverse_lazy("app_pages:PageListView") # Una vez demos click en el botón del formulario "page_confirm_delete.html", seremos
    # redireccionados a "PageListView".

"""
    MÁS INFORMACIÓN SOBRE ESTAS VISTAS EN:
    https://ccbv.co.uk/

    INTRODUCCIÓN A LAS VISTAS BASADAS EN CLASES:
    https://docs.djangoproject.com/en/3.1/topics/class-based-views/intro/
"""