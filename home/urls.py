from django.urls import path
from .views import home_view, user_view

app_name = 'home'

# /home
urlpatterns = [
    path('', home_view.home, name='index'),
    path('login/', user_view.login, name='login'),
    path('logout/', user_view.logout, name='logout'),
    path('register/', user_view.register, name='register'),
    path('list/', user_view.index, name='list'),
    path('edit/<int:pk>/', user_view.update, name='edit'),
        
    path('contracheque/', home_view.home, name='contracheque'),

    path('inserirpdf/', home_view.adicionar_contracheque, name='adicionar_pdf'),

    path('default/', home_view.default_page, name='defalt_page'),
]