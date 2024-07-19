# Generated by Django 4.2.13 on 2024-07-15 15:23
import json

from django.db import migrations, models
from django.db.models import QuerySet

from common.util.rsa_util import rsa_long_encrypt
from setting.models import Status, PermissionType
from smartdoc.const import CONFIG

default_embedding_model_id = '42f63a3d-427e-11ef-b3ec-a8a1595801ab'


def save_default_embedding_model(apps, schema_editor):
    ModelModel = apps.get_model('setting', 'Model')
    cache_folder = CONFIG.get('EMBEDDING_MODEL_PATH')
    model_name = CONFIG.get('EMBEDDING_MODEL_NAME')
    credential = {'cache_folder': cache_folder}
    model_credential_str = json.dumps(credential)
    model = ModelModel(id=default_embedding_model_id, name='maxkb-embedding', status=Status.SUCCESS,
                       model_type="EMBEDDING", model_name=model_name, user_id='f0dd8f71-e4ee-11ee-8c84-a8a1595801ab',
                       provider='model_local_provider',
                       credential=rsa_long_encrypt(model_credential_str), meta={},
                       permission_type=PermissionType.PUBLIC)
    model.save()


def reverse_code_embedding_model(apps, schema_editor):
    ModelModel = apps.get_model('setting', 'Model')
    QuerySet(ModelModel).filter(id=default_embedding_model_id).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('setting', '0004_alter_model_credential'),
    ]

    operations = [
        migrations.AddField(
            model_name='model',
            name='permission_type',
            field=models.CharField(choices=[('PUBLIC', '公开'), ('PRIVATE', '私有')], default='PRIVATE', max_length=20,
                                   verbose_name='权限类型'),
        ),
        migrations.RunPython(save_default_embedding_model, reverse_code_embedding_model)
    ]