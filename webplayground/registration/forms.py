from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserCreationFormWithEmail(UserCreationForm):
    """
    Extendemos el diccionario "UserCreationForm". Es decir, heredamos las propiedades de este para implementar nuevos campos, etc.
    """
     # Definimos un nuevo campo para almacenar el "email":
    email = forms.EmailField(required=True, help_text="Campo Requerido. Máximo 254 caracteres. Ingresa Email válido.")

    # El argument "help_text" nos ayudará a mostrar un texto de ayuda debajo del widget del respectivo campo.

    class Meta:
        model = User # Indicamos que modelo usar para construir el form. Django inspeccionará el modelo para construir el form de manera dinámica.
        fields = ("username", "email", "password1", "password2") # Agregamos los campos propios contenidos en el form "UserCreationForm" e 
        # implementamos nuestro nuevo campo "email". Recordemos que no es necesario agregar todos los campos en "fields" del modelo del que estamos
        # heredando, solo aquellos que vamos a requirir. Para este caso, requerimos todos los campos dentro del form/modelo "UserCreationForm" más
        # nuestro campo "email".

    def clean_email(self): # Para validar un campo directamente en el formulario, debemos declarar esta función. Debe de llamarse así forsozamente (clean_email).
        email = self.cleaned_data.get("email") # De esta manera recuperamos el valor del campo "email" del formulario actual.
        if User.objects.filter(email=email).exists(): # "User.objects.filter()" nos devuelve un QuerySet con los Usuarios filtrados por email.
            # Es importante que se use ".filter()" dado que de otra forma, no podremos hacer uso del método "exists()" para comprobar si existen
            # usuarios previamente registrados con dicho email. Si hacemos uso de ".get()", este sólo nos permite recuperar un usuario y sus 
            # atributos, de haber más de un usuario con el mismo "email", tendremos errores. Además, aunque sólo hubiese un usuario con el mismo nombre,
            # este no cuenta con el método "exists()", cosa que el QuerySet con ".filter()" sí cuenta. 
            raise forms.ValidationError("Este Email ya esta registrado, prueba con otro.") # En caso de que exista un usuario previamente registrado
            # con dicho "email", el registro no procederá, desplegando este mensaje y deberemos hacer uso de un nuevo email para el nuevo usuario.
        else:
            return email # Si el email a registrar nunca antes ha sido usado por ningun otro usuario ya registrado, procedemos con el registro. Siempre
            # y cuando los demás campos sean correctamente validados.

    # NOTA: Dado que el campo "email" ya se encuentra contenido dentro del model "User", podemos nostros asignar el valor que el usuario añada
    # a este campo directamente al campo "email". De otro forma, no tendría sentido agregar campos que no se encuentruen en el modelo "User". 
    # Ya que no nos servirian de nada. Por otro lado, "password1" y "password2" aunque no se encuentran de manera directa en como campos dentro
    # del modelo "User", una vez validado el formulario, podemos el valor de cualquiera de estos dos campos (ya que el valor debe ser exactamente
    # el mismo), a "password" el cual sí es un campo de "User". "username" ya se encuentra de manera directa en "User".

    # A continuación, muestro los campos propios del modelo "User":
    """
        auth.User.id
        auth.User.password
        auth.User.last_login
        auth.User.is_superuser
        auth.User.username
        auth.User.first_name
        auth.User.last_name
        auth.User.email
        auth.User.is_staff
        auth.User.is_active
        auth.User.date_joined
    """

    # NOTA 2: Si nosotros declaresemos de manera directa el atributo "widgets" (como lo hacemos en "forms.py" de la app pages), estariamos
    # machacando y sobreescribiendo todas las validaciones y configuraciones que ya contiene el formulario "UserCreationForm" (las cuales
    # son de grandísima ayuda), por lo que no es conveniente declarar el atributo "widgets" de manera directa. Por esta razón, hemos decido
    # modificar el formulario directamente en tiempo de ejcución desde el método "get_form()" (el cual se encuentra en "views.py"), para evitar
    # sobreescribir lo que ya se mencionó.

# 2DO FORMULARIO:
from .models import Profile
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile # De esta forma, obtendremos todos las instancias creadas a partir del modelo "Profile".
        fields = ["avatar", "bio", "link"]
        widgets = {
            "avatar": forms.ClearableFileInput(attrs={"class":"form-control-file mt-3"}),
            "bio": forms.Textarea(attrs={"class":"form-control mt-3", "rows":3, "placeholder":"Biografía"}),
            "link": forms.URLInput(attrs={"class":"form-control mt-3", "placeholder":"Enlace"}),
        }

    # NOTA 3: CADA QUE CREAMOS UN FORMULARIO A PARTIR DE UN MODELO/FORMULARIO PREDIFINIDO POR DJANGO (User, UserCreationForm) NO DEBEMOS
    #         DECLARAR EL ATRIBUTO "widgets" DE MANERA DIRECTA EN EL ARCHIVO "forms.py", DEBIDO A QUE MACHACAMOS Y SOBRESCRIBIMOS LAS VALIDACIONES
    #         ETC. QUE ESTOS MODELOS/FORMULARIOS YA TIENEN POR DEFECTO Y QUE SON DE GRAN AYUDA. EN SU LUGAR, SI SE DESEAN MODIFICAR LOS WIDGETS,
    #         ESTOS SE DEBEN MODIFICAR EN TIEMPOS DE EJECUCIÓN. Un ejemplo claro de esto se aprecia en "views.py" de esta misma aplicación. Para
    #         ser más exactos, en "SignUpView(CreateView)".

# 3ER FORMULARIO (Para editar email de nuestro usuario):
class EmailForm(forms.ModelForm):
    email = forms.EmailField(required=True, help_text="Campo Requerido. Máximo 254 caracteres. Ingresa Email válido.")
    class Meta:
        model = User
        fields = ["email"]
    
    def clean_email(self): # Con este método validamos un campo directamente en el formulario.
        email = self.cleaned_data.get("email")
        if "email" in self.changed_data: # "change_data" es una lista que almacena todos los campos que se han editado en el formulario.
            # Por ende, si dentro de esta lista se encuentra "email", significará que este campo ha sido editado.
            if User.objects.filter(email=email).exists(): # Verificamos si existe otro email identico al registrado.
                raise forms.ValidationError("Este Email ya esta registrado, prueba con otro.") # En caso de que el email registrado ya exista, lanzamos este error.
        return email # Si el email editado no es identico a los ya registrados, se retorna.