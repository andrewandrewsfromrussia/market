from django.core.management.base import BaseCommand
from django.core.management import call_command
from catalog.models import Product, Category

class Command(BaseCommand):
    help = "Очищает таблицы и загружает тестовые данные из фикстур"

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Удаляю старые данные..."))
        Product.objects.all().delete()
        Category.objects.all().delete()

        self.stdout.write(self.style.SUCCESS("Загружаю фикстуры..."))
        call_command("loaddata", "catalog/fixtures/categories.json")
        call_command("loaddata", "catalog/fixtures/products.json")

        self.stdout.write(self.style.SUCCESS(
            f"Готово: {Category.objects.count()} категорий, {Product.objects.count()} товаров"
        ))
