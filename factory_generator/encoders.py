from django.core.serializers.json import DjangoJSONEncoder
from django.core.files.base import File

import os


class DjangoFileJsonEncoder(DjangoJSONEncoder):
    """
    Extends DjangoJSONEncoder.
    It returns absolute path to file for django.core.files.base.File
    """
    def default(self, obj):
        if isinstance(obj, File):
            return os.path.realpath(obj.name)
        return super().default(obj)