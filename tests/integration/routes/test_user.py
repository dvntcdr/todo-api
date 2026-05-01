from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User
from tests.factories import USER_PASSWORD, UserFactory


class TestGetCurrentUser:
    URL: str = '/v1/users/me'

    async def test_success(self, user: User, client: AsyncClient, auth_headers):
        response = await client.get(self.URL, headers=auth_headers)
        data = response.json()

        assert response.status_code == 200
        assert data['username'] == user.username

    async def test_requires_auth(self, client: AsyncClient):
        response = await client.get(self.URL)
        assert response.status_code == 401


class TestChangeUsername:
    URL: str = '/v1/users/change-username'

    def _get_update_data(self, **kwargs) -> dict[str, str]:
        return {
            'password': kwargs.get('password', USER_PASSWORD),
            'new_username': kwargs.get('new_username', 'updated_username')
        }

    async def test_success(self, client: AsyncClient, auth_headers):
        update_data = self._get_update_data()

        response = await client.patch(
            self.URL, json=update_data, headers=auth_headers
        )
        data = response.json()

        assert response.status_code == 200
        assert data['username'] == update_data['new_username']

    async def test_wrong_password(self, client: AsyncClient, auth_headers):
        update_data = self._get_update_data(password='somepassword')

        response = await client.patch(
            self.URL, json=update_data, headers=auth_headers
        )

        assert response.status_code == 401

    async def test_same_username(self, user: User, client: AsyncClient, auth_headers):
        update_data = self._get_update_data(new_username=user.username)

        response = await client.patch(
            self.URL, json=update_data, headers=auth_headers
        )

        assert response.status_code == 400

    async def test_username_taken(self, db_session: AsyncSession, client: AsyncClient, auth_headers):
        other_user = UserFactory.build()
        update_data = self._get_update_data(new_username=other_user.username)

        db_session.add(other_user)
        await db_session.commit()

        response = await client.patch(
            self.URL, json=update_data, headers=auth_headers
        )

        assert response.status_code == 400


class TestChangeEmail:
    URL: str = '/v1/users/change-email'

    def _get_update_data(self, **kwargs) -> dict[str, str]:
        return {
            'password': kwargs.get('password', USER_PASSWORD),
            'new_email': kwargs.get('new_email', 'updated_email@example.com')
        }

    async def test_success(self, client: AsyncClient, auth_headers):
        update_data = self._get_update_data()

        response = await client.patch(
            self.URL, json=update_data, headers=auth_headers
        )
        data = response.json()

        assert response.status_code == 200
        assert data['email'] == update_data['new_email']

    async def test_wrong_password(self, client: AsyncClient, auth_headers):
        update_data = self._get_update_data(password='somepassword')

        response = await client.patch(
            self.URL, json=update_data, headers=auth_headers
        )

        assert response.status_code == 401

    async def test_same_email(self, user: User, client: AsyncClient, auth_headers):
        update_data = self._get_update_data(new_email=user.email)

        response = await client.patch(
            self.URL, json=update_data, headers=auth_headers
        )

        assert response.status_code == 400

    async def test_email_taken(self, db_session: AsyncSession, client: AsyncClient, auth_headers):
        other_user = UserFactory.build()
        update_data = self._get_update_data(new_email=other_user.email)

        db_session.add(other_user)
        await db_session.commit()

        response = await client.patch(
            self.URL, json=update_data, headers=auth_headers
        )

        assert response.status_code == 400
