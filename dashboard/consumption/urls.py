from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name="index"),
    url(r'^summary/', views.summary, name="summary"),
    url(r'^detail/([0-9]+)/$', views.detail, name="detail"),
    url(r'^api/total/$', views.TotalChartData.as_view(), name="total"),
    url(r'^api/average/$', views.AverageChartData.as_view(), name="average"),
    url(r'^api/consumers/$', views.ConsumerChartData.as_view(),
        name="consumers"),

]
