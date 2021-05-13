from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group, Permission
from stores.models import Store, Pizza, StoreIngredients, PizzaIngredients
from utils.permissions import get_permission_names


class Command(BaseCommand):
    _store_owners_group_name = 'Store Owners'

    @staticmethod
    def _get_store_owners_group():
        try:
            store_owners_group = Group.objects.get(name=Command._store_owners_group_name)
        except Group.DoesNotExist:
            permission_names = get_permission_names([Store, Pizza, StoreIngredients, PizzaIngredients])
            permissions = Permission.objects.filter(codename__in=permission_names)

            store_owners_group = Group(name=Command._store_owners_group_name)
            store_owners_group.save()

            store_owners_group.permissions.set(permissions)

        return store_owners_group

    def handle(self, *args, **kwargs):
        store_owners_group = Command._get_store_owners_group()
        
        try:
            stores = Store.objects.all()
            for store in stores:
                if len(store.owner.groups.filter(name=Command._store_owners_group_name)) == 0:
                    store.owner.groups.add(store_owners_group)
        except BaseException as e:
            raise CommandError(e)
