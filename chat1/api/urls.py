from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)




urlpatterns = [
    path('login',views.login,name='login'),
    path('signup',views.signup,name='signup'),
    path('start/<str:id>',views.start_chat),
    path('users',views.get_active_users),

    
    # path('/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]

