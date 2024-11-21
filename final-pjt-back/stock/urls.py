from django.urls import path
from . import views

urlpatterns = [
    path('token/',views.get_token),
    path('stock/analyze/',views.analyze),
    path('stock/indus_chart/',views.draw_theme_chart),
    path('stock/d_chart_and_data/',views.d_chart_and_data),
    path('stock/o_chart_and_data/',views.o_chart_and_data),
    path('stock/d_chart_period/',views.d_chart_period),
    path('stock/o_chart_period/',views.o_chart_period),
    path('stock/same_mbti/',views.get_same_mbti_theme),
]