from django.conf.urls import url
from . import views
# from django.contrib import admin

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^register$', views.register, name="register"),
    url(r'^show$', views.show, name="show"),
    url(r'^success$', views.success, name="success"),
    url(r'^show/(?P<id>\d+)/delete$', views.destroy, name="destroy"),
    url(r'^login$', views.login, name="login"),
    # url(r'^admin/', admin.site.urls),
]
