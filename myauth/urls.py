from django.urls import path
from .views import *

urlpatterns=[
    path('', home, name="home"),
    path('login/', loginPage, name="loginPage"),
    path('logout/', logoutPage, name="logoutPage"),
    path('registernewuser/', registerNewUser, name="registerNewUser"),
    path('reports/', reports, name="reports"),
    path('getFeePaid/<str:pk>', getFeePaid, name="getFeePaid"),
    path('deletemember/<str:pk>', deleteMember, name="deleteMember"),
    path('dueMembers/', dueMembers, name="dueMembers"),
    path('bloodGroup/', bloodGroup, name="bloodGroup"),
    path('edit_member/<int:instance_id>/', edit_member, name='edit_member'),
]