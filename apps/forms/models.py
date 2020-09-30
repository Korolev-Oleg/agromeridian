from django.db import models


# Create your models here.
class Applications(models.Model):
    test_field = models.CharField(max_length=10, verbose_name='test field')

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    def __str__(self):
        return self.test_field
