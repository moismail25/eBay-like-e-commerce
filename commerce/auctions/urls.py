from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add", views.newListing, name="new"),
    path("<int:listing_id>", views.listing_view, name="listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("<int:listing_id>/watchlist", views.add_to_watchlist, name="add_to_watchlist"),
    path("<int:listing_id>/comment", views.comment, name="comment"),
    path("<int:listing_id>/bid", views.bid, name="bid"),
    path("categories", views.categories_view, name="categories"),
    path("category/<str:category>", views.category_view, name="category")

]
