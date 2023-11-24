from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('v1/books/', views.BookList.as_view(), name='book_list'),
    path('v1/books/<int:pk>/', views.BookDetail.as_view(), name='book_detail'),
    path('v1/allborrowed/', views.AllBorrowedList.as_view(), name='allborrowed_list'),
    path('v1/books/<uuid:pk>/renew/', views.RenewBook.as_view(), name='book_renew'),
]
