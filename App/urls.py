from django.urls import path
from App.views import index
from .views import DesignLoginView, register, DeleteRequestView, admin_category_add, category_list, AdminCategoryDelete, \
    request_all, ChangeStatusCompleted, ChangeStatusAcceptWork
from .views import DesignLogoutView
from .views import RegisterDoneView, RegisterUserView
from .views import profile
from .views import profile_request_add
from .views import other_page


app_name = 'App'

urlpatterns = [
    path('', index, name='index'),
    path('accounts/login', DesignLoginView.as_view(), name='login'),
    path('accounts/logout/', DesignLogoutView.as_view(), name='logout'),
    path('accounts/register/done/', RegisterDoneView.as_view(), name='register_done'),
    path('accounts/register/', register, name='register'),
    path('accounts/profile/', profile, name='profile'),
    # path('accounts/profile/change/', ChangeUserInfoView.as_view(), name='profile_change'),
    path('accounts/profile/add/', profile_request_add, name='profile_request_add'),
    # path('accounts/profile/delete/<int:id>/', profile_request_delete, name='profile_request_delete'),
    path('applications/delete/<int:pk>/', DeleteRequestView.as_view(), name='profile_request_delete'),
    path('category/add/', admin_category_add, name='admin_category_add'),
    path('category/delete/<int:id>', AdminCategoryDelete.as_view(), name='admin_category_delete'),
    path('category/list/', category_list, name='category_list'),
    path('request/all/', request_all, name='request_all'),
    path('change/status/completed/<int:id>/', ChangeStatusCompleted.as_view(), name='change_status_completed'),
    path('change/status/accept/work/<int:id>/', ChangeStatusAcceptWork.as_view(), name='change_status_accept_work'),
    # path('<int:pk>/', rubric, name='rubric'),
    # path('accounts/profile/delete/', DeleteUserView.as_view(), name='profile_delete'),
    # path('<str:page>/', other_page, name='other'),
]