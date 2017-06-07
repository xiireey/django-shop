# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from djng.models.fields import ImageField
from shop.models.customer import BaseCustomer


class Customer(BaseCustomer):
    """
    Customer model with avator support.
    """
    SALUTATION = [('mrs', _("Mrs.")), ('mr', _("Mr.")), ('na', _("(n/a)"))]

    number = models.PositiveIntegerField(
        _("Customer Number"),
        null=True,
        default=None,
        unique=True,
    )

    salutation = models.CharField(
        _("Salutation"),
        max_length=5,
        choices=SALUTATION,
    )

    avatar = ImageField(
        _("Your Photo"),
        blank=True,
        upload_to='myshop',
    )

    def get_number(self):
        return self.number

    def get_or_assign_number(self):
        if self.number is None:
            aggr = Customer.objects.filter(number__isnull=False).aggregate(models.Max('number'))
            self.number = (aggr['number__max'] or 0) + 1
            self.save()
        return self.get_number()
