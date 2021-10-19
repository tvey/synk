import pytest
from rest_framework.authtoken.models import Token

pytestmark = [pytest.mark.django_db(transaction=True)]


class TestUserModel:
    def test_user_attributes(self, user):
        assert hasattr(user, 'username')
        assert hasattr(user, 'email')

    def test_user_api_token_created(self, user):
        assert Token.objects.filter(user=user)

    def test_str(self, user):
        assert str(user) == f'({user.username}, {user.email})'
