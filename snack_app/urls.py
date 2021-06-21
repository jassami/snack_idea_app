from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('create', views.create),
    path('delete/<int:snack_id>', views.delete),
    path('<int:snack_id>', views.snack),
    path('users/<int:user_id>', views.users),
    path('users/update', views.update),
    path('like/<int:snack_id>', views.like),
    path('dislike/<int:snack_id>', views.dislike),
]