from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html


# Register your models here.
from .models import Municipio, Edital, Produto, Item, Preco
from .forms import ItemForm


class MunicipioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'view_editais')  # Include the custom method in list display

    def view_editais(self, obj):
        """Generate HTML links to the Edital objects related to this Municipio."""
        editais = Edital.objects.filter(municipio=obj)
        links = []
        for edital in editais:
            url = reverse('admin:editais_edital_change', args=[edital.id])
            link = format_html('<a href="{}">{}</a>', url, edital)
            links.append(link)
        return format_html('<br>'.join(links))

    view_editais.short_description = 'Editais'
    change_list_template = "admin/change_list.html"
    
class ItemInline(admin.TabularInline):
    model = Item
    extra = 1
    form = ItemForm
    classes = ('grp-collapse grp-open',)

class EditalAdmin(admin.ModelAdmin):
    inlines = [ItemInline]
    list_display = ('municipio', 'data_pregao') 
    

class PrecoInline(admin.TabularInline):
    model = Preco
    extra = 0
class ProdutoAdmin(admin.ModelAdmin):
    inlines = (PrecoInline,)



admin.site.site_header = "Controle de Editais Nutri C"
admin.site.register(Municipio, MunicipioAdmin)
admin.site.register(Edital, EditalAdmin)
admin.site.register(Produto, ProdutoAdmin)
