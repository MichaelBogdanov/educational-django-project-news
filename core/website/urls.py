from django.conf import settings
from django.urls import path
from .views import *
from django.conf.urls.static import static

urlpatterns = [
    path('', index),
    path('login/', login_view),
    path('register/', register_view),
    path('logout/', logout_view),
    path('category/<int:id>/', index),
    path('news/<int:id>/', news),
    path('profile/', profile),
    path('delete_comment/<int:id>/', profile)
]
