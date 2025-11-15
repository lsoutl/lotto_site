from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('my/tickets/', views.my_tickets, name='my_tickets'),
    path("buy/<int:draw>/auto/", views.buy_auto, name="buy_auto"),
    path("buy/<int:draw>/manual/", views.buy_manual, name="buy_manual"),
    path("draw/<int:draw>/result/", views.draw_result, name="draw_result"),
]