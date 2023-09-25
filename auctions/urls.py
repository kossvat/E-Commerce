from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create_listing"),
    path("listing/<int:listing_id>", views.listing_details, name="listing_details"),
    path("add_to_watchlist/<int:listing_id>", views.add_to_watchlist, name="add_to_watchlist"),
    path("remove_from_watchlist/<int:listing_id>", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("my_watchlist", views.users_watchlist, name="user_watchlist"),
    path('listing/<int:listing_id>/bid/', views.place_bid, name='place_bid'),
    path('listing/<int:listing_id>/end/', views.end_auction, name='end_auction'),
    path('categories', views.category_list, name='category_list'),
    path('categories/<int:category_id>', views.category_listing, name='category_listings'),
    path('edit_listing/<int:listing_id>', views.edit_listing, name='edit_listing'),
    path('closed_listing', views.closed_listings, name='closed_listings')
]
