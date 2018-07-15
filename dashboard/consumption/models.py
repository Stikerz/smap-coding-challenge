# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db.models import Sum, Avg, IntegerField
from django.db import models
from collections import defaultdict
import calendar
# Create your models here.

class Consumers(models.Model):
    AREA = (('a1', 'Area_1'), ('a2', 'Area_2'))
    TARIFF = (('t1', 'Tariff_1'), ('t2', 'Tariff_2'), ('t3', 'Tariff_3'))

    id = models.IntegerField(primary_key=True, blank=False)
    area = models.CharField(max_length=2, choices=AREA, blank=False,)
    tariff = models.CharField(max_length=2, choices=TARIFF, blank=False,)

    def __str__(self):
        return "Comsumer {}".format(self.id)

class Consumption(models.Model):
    consumer_id = models.ForeignKey(Consumers, on_delete=models.CASCADE)
    date_time = models.DateTimeField(blank=False,)
    consumption = models.DecimalField(blank=False,
                                      decimal_places=2, max_digits=6)

    def __str__(self):
        return "Consumption {} Comsumer {}".format(self.id, self.consumer_id)

    @classmethod
    def get_average(cls, consumer=None):

        if consumer:
            consumptions = Consumption.objects.filter(consumer_id=consumer)
        else:
            consumptions = Consumption.objects.all()


        energy_data = defaultdict(int)

        years = [d.year for d in
                 consumptions.datetimes('date_time', 'year')]

        months = [d.month for d in
                  consumptions.datetimes('date_time', 'month')]

        for year in years:
            for month in months:
                month_average = consumptions.filter(date_time__year=year,
                                           date_time__month=month
                                           ).aggregate(Avg(
                    'consumption', output_field=IntegerField()))

                txt_month = calendar.month_abbr[month]
                energy_data[txt_month] = month_average['consumption__avg']

        return energy_data

    @classmethod
    def get_total(cls, consumer=None):

        if consumer:
            consumptions = Consumption.objects.filter(consumer_id=consumer)
        else:
            consumptions = Consumption.objects.all()

        energy_data = defaultdict(float)

        years = [d.year for d in
                 consumptions.datetimes('date_time', 'year')]

        months = [d.month for d in
                  consumptions.datetimes('date_time', 'month')]

        for year in years:
            for month in months:
                month_sum = consumptions.filter(date_time__year=year,
                                                date_time__month=month
                                                ).aggregate(Sum(
                    'consumption'))

                txt_month = calendar.month_abbr[month]
                energy_data[txt_month]= float(month_sum['consumption__sum'])

        return energy_data
