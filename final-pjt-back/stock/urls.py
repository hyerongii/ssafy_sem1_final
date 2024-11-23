from django.urls import path
from . import views

urlpatterns = [
    path('token/',views.get_token),
    path('stock/analyze/',views.analyze),
    path('stock/indus_chart/',views.draw_theme_chart),
    path('stock/d_chart/',views.d_chart),
    path('stock/d_main_data/',views.d_main_data),
    path('stock/o_chart/',views.o_chart),
    path('stock/o_main_data/',views.o_main_data),
    path('stock/d_chart_period/',views.d_chart_period),
    path('stock/o_chart_period/',views.o_chart_period),
    path('stock/same_mbti/',views.get_same_mbti_theme),
    path('stock/article/create/',views.create_stock_article),
    path('stock/article/update_or_delete/',views.stock_article_delete_or_put),
    # 아래의 호출로 article detail로 이동 및 해당 게시글의 comment 전달
    path('stock/article/<int:article_pk>/',views.get_stock_article_detail),
    path('stock/article/<int:comment_pk>/',views.comment_update_delete),
]
