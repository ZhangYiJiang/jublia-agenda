from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __iter__(self):
        for field in self._meta.get_fields():
            value = getattr(self, field.name, None)
            yield (field.name, value)

    class Meta:
        abstract = True
