from django.conf import settings
from django.db import migrations


def fill_owner_forward(apps, schema_editor):
    Product = apps.get_model("catalog", "Product")

    app_label, model_name = settings.AUTH_USER_MODEL.split(".")
    User = apps.get_model(app_label, model_name)

    # Берём самого раннего пользователя как технического владельца
    fallback_user = User.objects.order_by("pk").first()
    if fallback_user is None:
        # Если пользователей нет, просто выходим; позже поле делать non-null нельзя,
        # пока не создашь хотя бы одного пользователя.
        return

    Product.objects.filter(owner__isnull=True).update(owner=fallback_user)


def fill_owner_backward(apps, schema_editor):
    # Откат намеренно пустой
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0004_alter_product_options_product_status"),
    ]

    operations = [
        migrations.RunPython(fill_owner_forward, fill_owner_backward),
    ]
