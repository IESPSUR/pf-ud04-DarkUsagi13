# Generated by Django 4.1.3 on 2022-11-13 13:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0005_rename_compras_compra'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compra',
            name='nombre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tienda.producto'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='marca',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tienda.marca'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='modelo',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='producto',
            name='nombre',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='producto',
            name='unidades',
            field=models.IntegerField(default=0),
        ),
    ]
