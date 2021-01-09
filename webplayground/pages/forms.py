from django import forms

# Creating a form using "forms.ModelForm"
from .models import Page
class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ("title", "content", "order") # El tipo de dato de cada columna, etc. Es tomado del respectivo campo en el modelo "Page".
        
        # Sobreescribimos el default "widget" de cada campo que utilizaremos con la finalidad de mostrarlo más estético:
        widgets = {
            "title":forms.TextInput(attrs={"class":"form-control"}), # "<campo>":<nuevo_widget>(attrs={configuración}).
            "content":forms.Textarea(attrs={"class":"form-control"}), # "<campo>":<nuevo_widget>(attrs={"class":"boot-strap class para forms"}).
            "order":forms.NumberInput(attrs={"class":"form-control"}),
        }

        """
        Si deseamos "editar el nombre de las etiquetas" para que se muestre de una forma diferente en el formulario o en su defecto que el nombre
        de estos campos no se muestre en el formulario, debemos hacer uso del atributo "labels" e igualarlo a un diccionario. Esto, se muestra
        a continuación:

        labels = {
            # <campo>:"<nombre_a_mostrar>" o <campo>:''; para no mostrar el nombre del campo en el formulario.
            "title":"TÍTULO", # Se mostrará "TÍTULO" en lugar de "Título" (que corresponde al valor asignado al "verbose_name" del campo dentro de "models.py").
            "content": "CONTENDIO", # Se mostrará "CONTENIDO" en lugar de "Contenido" (que corresponde al valor asignado al "verbose_name" del campo dentro de "models.py").
            "order": '', # No se mostrará el nombre del campo en el formulario.
        }
        """