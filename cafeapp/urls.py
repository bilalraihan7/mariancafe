from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('detail/<int:pk>/',views.details_vehicle),
    path('foodmenu',views.Allfood),
    path('staff_register/',views.staff_registration, name='staff_registration'),
    path('login',views.login,name='login'),
    path('view_license/<int:id>/', views.view_license, name='view_license'),
    path('view_license2/<int:id>/', views.view_user_license, name='view_license2'),
    path('services',views.services),
    path('user_home',views.user_home),
    path('logout/', views.logout_view, name='logout'),
    path('staff_home',views.staff_home),
    path('add_menu',views.add_food),
    path('delete_food/<int:id>/',views.delete_food),
    path('filter/<int:fid>/',views.filter),
    path('drivers',views.view_drivers),
    path('search_food',views.search_food,name='search_food'),
    path('book_vehicle/<int:vehicle_id>/',views.book_vehicle),
    path('viewbookings',views.view_booking),
    path('mybookings',views.my_booking),
    path('stats',views.view_stats),
    path('make_payment/<int:booking_id>/', views.make_payment, name='make_payment'),
    path('edit-user',views.edituser),
    path('changep-user',views.changepassword_user),
    path('edit-driver',views.editdriver),
    path('changep-driver',views.changepassword_driver),
    path('uview_drivervehicle/<int:did>/',views.view_driver_vehicles)
]
    

