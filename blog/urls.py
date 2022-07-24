
from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.post_list,name="post_list"),
    path('add', views.vm_add,name="vm_add"),
    path('start', views.start_vm),
    path('stop', views.stop_vm,name="stop_vm"),
    path('showvm', views.show_vm),
    path('destroy', views.destroy_vm),
    path('reboot', views.reboot_vm),
    path('docker/vm', views.docker_vm),
    path('details', views.details),
]
