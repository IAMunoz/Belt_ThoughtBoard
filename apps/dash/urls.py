from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard),
    path('make_th', views.make_thought),
    path('<int:tid>', views.detail),
    path('like/<int:tid>', views.like),
    path('dislike/<int:tid>', views.dislike),
    path('delete/<int:tid>', views.delete),
]