from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("cards/", views.cards, name="cards"),
    path("totals/", views.totals, name="totals"),
    path("cards/<int:card_id>/delete", views.del_card, name="del_card"),
    path("card/<int:card_id>/edit", views.edit_card, name="edit_card"),
]