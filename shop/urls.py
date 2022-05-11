from django.urls import path
from django.views.generic import TemplateView

from .views import DetailView, SignupView, LoginView, LogoutView, CartView, CheckOutView, OrderView

home_view = TemplateView.as_view(template_name="index.html")

urlpatterns = [
    path("", home_view, name="home"),
    path("signup", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("detail/", DetailView.as_view(), name="detail"),
    path("cart/", CartView.as_view(), name="cart"),
    path("checkout", CheckOutView.as_view(), name="checkout"),
    path("order", OrderView.as_view(), name="order"),
]
