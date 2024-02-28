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
    path('search_food',views.search_food,name='search_food'),
    path('mybookings',views.myBookings),
    path('edit-user',views.edituser),
    path('changep-user',views.changepassword_user),
    path('edit-staff',views.editstaff),
    path('changep-staff',views.changepassword_staff),
    path('addToCart/<int:food_id>/',views.addToCart),
    path('removeFromCart/<int:food_id>/',views.removeFromCart),
    path('checkout/', views.checkout, name='checkout'),
    path('payment/', views.payment, name='payment'),
    path('confirm_checkout/', views.confirm_checkout, name='confirm_checkout'),
    path('increase_quantity/<int:food_id>/',views.increaseQuantity, name='increase_quantity'),
    path('decrease_quantity/<int:food_id>/',views.decreaseQuantity, name='decrease_quantity'),
    path('edit_food/<int:foodid>/',views.update_foodDetails,name='edit_food'),
    path('viewbookings',views.viewBookingsStaff),
]
    

