# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from .models import Consumption, Consumers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication
from collections import defaultdict

# Create your views here.

def home(request):
    context = {
    }
    return render(request, 'consumption/base.html', context)


def summary(request):
    template = 'consumption/summary.html'
    query_set = Consumers.objects.all()
    query = request.GET.get("query")
    if query:
        query_set = query_set.filter(id=query)
    paginator = Paginator(query_set, 10)
    page = request.GET.get('page')

    try:
        object_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        object_list = paginator.page(1)

    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        object_list = paginator.page(paginator.num_pages)


    context = {'object_list': object_list, "lala":'land'}
    return render(request, template, context)

def detail(request, id):
    template = 'consumption/detail.html'
    consumption_data = Consumption.objects.filter(consumer_id=id)
    consumer = get_object_or_404(Consumers, id=id)

    query = request.GET.get("query")
    if query:
        consumption_data = consumption_data.filter(date_time__contains=query)
    paginator = Paginator(consumption_data, 25)
    page = request.GET.get('page')

    try:
        object_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        object_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        object_list = paginator.page(paginator.num_pages)

    context = {'object_list': object_list, 'user_data':consumer}
    return render(request, template, context)


class TotalChartData(APIView):
    authentication_classes = [authentication.BasicAuthentication]

    def get(self, *args, format=None):
        labels = []
        total = []
        data = Consumption.get_total()

        if args:
            print(args)

        for key, value in data.items():
            labels.append(key)
            total.append(value)

        chart_data = {"labels": labels,
                "totals": total}
        return Response(chart_data)


class AverageChartData(APIView):
    authentication_classes = [authentication.BasicAuthentication]

    def get(self, request, format=None):
        labels = []
        average = []
        data = Consumption.get_average()

        for key, value in data.items():
            labels.append(key)
            average.append(value)

        chart_data = {"labels": labels,
                "average": average}
        return Response(chart_data)

class ConsumerChartData(APIView):
    authentication_classes = [authentication.BasicAuthentication]

    def get(self, request, format=None):
        labels = []
        average = []
        total = []
        data= defaultdict(dict)
        all_consumers = Consumers.objects.all()
        for consumer in all_consumers:
            avg_data = Consumption.get_average(consumer=consumer)
            total_data = Consumption.get_total(consumer=consumer)

            for key, value in avg_data.items():
                labels.append(key)
                average.append(value)

            for key, value in total_data.items():
                total.append(value)

            data[consumer.id] ={"labels":labels,"average":average,
                                                   "total":total}
            labels = []
            average = []
            total = []
        return Response(data)

