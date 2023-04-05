from django.db.models import Model
from django.db.models.fields import UUIDField
from django.db.models.fields.related import ForeignKey


def model_to_dict(instance: Model, exclude_fields: list[str] = []):
    """
    Convert a model instance to a dictionary.

    params:
        instance: Model instance
        exclude_fields: list of fields to exclude from the dictionary
    """
    opts = instance._meta
    data = {}

    if not isinstance(exclude_fields, list):
        exclude_fields = []

    for f in opts.concrete_fields:
        if f.name in exclude_fields:
            continue
        if not f.editable and not isinstance(f, ForeignKey):
            continue
        if isinstance(f, ForeignKey) or isinstance(f, UUIDField):
            value = f.value_from_object(instance)
            if value:
                data[f.name] = str(value)
        else:
            data[f.name] = f.value_from_object(instance)
    return data
