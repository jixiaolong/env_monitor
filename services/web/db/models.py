from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext as _


class BaseModel(models.Model):
    create_time = models.DateTimeField(auto_created=True, auto_now=True)
    modified_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseInfo(BaseModel):
    base_num = models.CharField(max_length=32, null=False, verbose_name=_("base number"))

    sim_number = models.CharField(max_length=16, null=False, verbose_name=_("sim number"))
    sim_price = models.FloatField(default=0.0, verbose_name=_("the rest of sim price"))
    sim_type_info = models.TextField(max_length=128,
                                     verbose_name=_("the price of every month for this sim card"))

    monitor_place = models.TextField(max_length=256,
                                     verbose_name=_("the place of the device locate"))
    longitude = models.FloatField(verbose_name=_("the device's longitude"))
    latitude = models.FloatField(verbose_name=_("the device's latitude"))

    monitor_fields = models.CharField(max_length=256, null=False,
                                      verbose_name=_("the fields of monitor type"))
    current_status = models.TextField(verbose_name=_("the current situation of device "))

    class Meta:
        db_table = "base_info"
        ordering = ("-id", )

    def __str__(self):
        return "{base_num}: sim_number: {sim_number} sim_price:{sim_price}".format(
            base_num=self.base_num, sim_number=self.sim_number, sim_price=self.sim_price
        )

