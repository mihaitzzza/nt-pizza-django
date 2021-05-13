from django.contrib import admin
from django.utils.html import format_html
from stores.models import Store


def get_owner_fullname(obj):
    return '%s %s' % (obj.owner.first_name, obj.owner.last_name)


def get_logo(obj):
    return format_html('<img src="%s" width="50px" />' % obj.logo.url)


get_owner_fullname.short_description = 'Owner name'
get_logo.short_description = 'Logo'


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', get_owner_fullname, get_logo, 'delivery_fee', 'profit_fee')
    ordering = ('-created_at', '-updated_at')
    search_fields = ('name', 'owner__first_name', 'owner__last_name')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        if not request.user.is_superuser:
            return queryset.filter(owner=request.user)

        return queryset

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)

        if not request.user.is_superuser:
            fields.remove('owner')

        return fields

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.owner = request.user
        # if not form.cleaned_data.get('owner'):
        #     obj.owner = request.user

        super().save_model(request, obj, form, change)
