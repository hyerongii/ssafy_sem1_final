from django.urls import path
from . import views

urlpatterns = [
    path('token/',views.get_token),
    path('stock/analyze/',views.analyze),
    path('stock/indus_chart/',views.draw_theme_chart),
    path('stock/chart_and_data/',views.draw_theme_chart),
]