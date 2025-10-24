from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from catalog.models import Product


class Command(BaseCommand):
    help = "Создаёт группу 'Модератор продуктов' с нужными правами."

    def handle(self, *args, **options):
        group_name = "Модератор продуктов"
        group, created = Group.objects.get_or_create(name=group_name)

        # Кастомные права
        unpublish_perm = Permission.objects.get(
            codename="can_unpublish_product",
            content_type__app_label="catalog",
        )

        # Стандартное delete_product
        delete_perm = Permission.objects.get(
            codename="delete_product",
            content_type__app_label="catalog",
        )

        group.permissions.set([unpublish_perm, delete_perm])
        group.save()

        if created:
            self.stdout.write(self.style.SUCCESS(f"Группа '{group_name}' создана."))
        else:
            self.stdout.write(self.style.SUCCESS(f"Группа '{group_name}' обновлена."))
