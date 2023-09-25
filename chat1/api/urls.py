from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from rest_framework_swagger.views import get_swagger_view
schema_view = get_swagger_view(title='Pastebin API')


urlpatterns = [
    path('login',views.login,name='login'),
    path('signup',views.signup,name='signup'),
    path('start/<str:id>',views.start_chat),
    path('users',views.get_active_users),
    path('', schema_view)
    
    # path('/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]

