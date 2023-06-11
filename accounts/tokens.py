#this is used to generate tokens manually by django
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

User=get_user_model()

def create_jwt_paie_for_user(user:User):
    refresh=RefreshToken.for_user(user)
    tokens={
        'access':str(refresh.access_token),
        'refresh':str(refresh)
    }
    print(tokens)
    return tokens