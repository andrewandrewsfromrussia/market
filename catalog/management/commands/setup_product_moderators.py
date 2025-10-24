# catalog/management/commands/setup_product_moderators.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product


class Command(BaseCommand):
    help = "Создаёт группу «Модератор продуктов» и назначает нужные права"

    GROUP_NAME = "Модератор продуктов"
    PERMS = (
        ("can_unpublish_product", "catalog", "product"),
        ("delete_product", "catalog", "product"),
    )

    def handle(self, *args, **options):
        ct: ContentType = ContentType.objects.get_for_model(Product)

        group, created = Group.objects.get_or_create(name=self.GROUP_NAME)
        if created:
            self.stdout.write(self.style.SUCCESS(f"Создана группа: {group.name}"))
        else:
            self.stdout.write(self.style.WARNING(f"Группа уже существует: {group.name}"))

        perms_to_add = []
        for codename, app_label, model in self.PERMS:
            try:
                perm = Permission.objects.get(codename=codename, content_type=ct)
                perms_to_add.append(perm)
            except Permission.DoesNotExist:
                self.stdout.write(self.style.ERROR(
                    f"Право не найдено: {codename}. Убедись, что оно объявлено в Meta.permissions и применены миграции."
                ))

        if perms_to_add:
            group.permissions.add(*perms_to_add)
            self.stdout.write(self.style.SUCCESS("Права назначены."))

        self.stdout.write(self.style.SUCCESS("Готово."))
