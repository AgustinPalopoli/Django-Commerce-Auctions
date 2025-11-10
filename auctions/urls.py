from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("<int:auction_id>", views.view_listing, name="view_listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("remove_watchlist", views.remove_watchlist, name="remove_watchlist"),
    path("new_bid", views.new_bid, name="new_bid"),
    path("close_auction", views.close_auction, name="close_auction"),
    path("comment", views.comment, name="comment"),
    path("category", views.category, name="category"),
]
