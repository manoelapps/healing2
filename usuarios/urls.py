from django.urls import path
from . import views, htmx_views

urlpatterns = [
    path('cadastro/', views.cadastro, name="cadastro"),
    path('login/', views.login_view, name="login"),
    path('sair/', views.sair, name="sair"),
]

htmx_urlspatterns=[
    path('check_user/', htmx_views.check_user, name="check_user"),
    path('check_email/', htmx_views.check_email, name="check_email")
]

urlpatterns += htmx_urlspatterns