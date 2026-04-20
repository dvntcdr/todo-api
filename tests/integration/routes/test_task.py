from typing import Any
from uuid import uuid4

from httpx import AsyncClient

from src.models.project import Project
from src.models.task import Task, TaskPriority, TaskStatus
from src.models.user import User


class TestGetTasks:
    URL: str = '/v1/tasks/'

    async def test_success(self, task: Task, client: AsyncClient, auth_headers):
        response = await client.get(self.URL, headers=auth_headers)

        data = response.json()

        assert response.status_code == 200
        assert data['total'] >= 1
        assert len(data['items']) >= 1

    async def test_requires_auth(self, client: AsyncClient):
        response = await client.get(self.URL)
        assert response.status_code == 401

    async def test_filter_by_status(self, task: Task, client: AsyncClient, auth_headers):
        response = await client.get(
            self.URL, params={'status': task.status.value}, headers=auth_headers
        )

        data = response.json()

        assert response.status_code == 200
        assert all(t['status'] == task.status.value for t in data['items'])

    async def test_filter_by_project(self, user: User, task: Task, project: Project, client: AsyncClient, auth_headers):
        response = await client.get(
            self.URL, params={'project_id': str(project.id)}, headers=auth_headers
        )

        data = response.json()

        assert response.status_code == 200
        assert all(t['project_id'] == str(project.id) for t in data['items'])


class TestGetTask:
    URL: str = '/v1/tasks/{}'

    async def test_success(self, task: Task, client: AsyncClient, auth_headers):
        response = await client.get(
            self.URL.format(str(task.id)), headers=auth_headers
        )

        assert response.status_code == 200
        assert response.json()['id'] == str(task.id)

    async def test_not_found(self, client: AsyncClient, auth_headers):
        response = await client.get(
            self.URL.format(str(uuid4())), headers=auth_headers
        )
        assert response.status_code == 404

    async def test_not_owned(
        self,
        user: User,  # noqa
        task: Task,
        client: AsyncClient,
        second_auth_headers
    ):
        response = await client.get(
            self.URL.format(str(task.id)), headers=second_auth_headers
        )

        assert response.status_code == 403


class TestCreateTask:
    URL: str = '/v1/tasks/'

    def _get_task_data(self, **kwargs) -> dict[str, Any]:
        return {
            'title': kwargs.get('title', 'Test task'),
            'description': kwargs.get('description', 'Test task description'),
            'project_id': kwargs.get('project_id', None)
        }

    async def test_create(self, user: User, project: Project, client: AsyncClient, auth_headers):
        task_data = self._get_task_data(project_id=str(project.id))

        response = await client.post(
            self.URL, json=task_data, headers=auth_headers
        )
        data = response.json()

        assert response.status_code == 201
        assert data['title'] == task_data['title']
        assert data['description'] == task_data['description']
        assert data['owner_id'] == str(user.id)
        assert data['project_id'] == str(project.id)

    async def test_requires_auth(self, client: AsyncClient):
        response = await client.post(self.URL, json=self._get_task_data())
        assert response.status_code == 401

    async def test_project_not_found(self, client: AsyncClient, auth_headers):
        task_data = self._get_task_data(project_id=str(uuid4()))
        response = await client.post(self.URL, json=task_data, headers=auth_headers)
        assert response.status_code == 404

    async def test_project_not_owned(
        self,
        project: Project,
        client: AsyncClient,
        second_auth_headers
    ):
        task_data = self._get_task_data(project_id=str(project.id))
        response = await client.post(self.URL, json=task_data, headers=second_auth_headers)

        assert response.status_code == 403


class TestUpdateTask:
    URL: str = '/v1/tasks/{}'

    def _get_update_task_data(self, **kwargs) -> dict[str, Any]:
        return {
            'title': kwargs.get('title', 'Updated task title'),
            'description': kwargs.get('description', 'Updated task description'),
            'status': kwargs.get('status', TaskStatus.ACTIVE.value),
            'priority': kwargs.get('description', TaskPriority.HIGH.value),
            'due_date': kwargs.get('description', '2026-12-12T00:00:00'),
        }

    async def test_success(self, task: Task, client: AsyncClient, auth_headers):
        task_data = self._get_update_task_data()
        response = await client.patch(
            self.URL.format(str(task.id)), json=task_data, headers=auth_headers
        )

        data = response.json()

        assert response.status_code == 200
        for field, value in task_data.items():
            assert data[field] == value

    async def test_not_found(self, client: AsyncClient, auth_headers):
        task_data = self._get_update_task_data()
        response = await client.patch(
            self.URL.format(str(uuid4())), json=task_data, headers=auth_headers
        )

        assert response.status_code == 404

    async def test_not_owned(
        self,
        task: Task,
        client: AsyncClient,
        second_auth_headers
    ):
        task_data = self._get_update_task_data()
        response = await client.patch(
            self.URL.format(str(task.id)), json=task_data, headers=second_auth_headers
        )

        assert response.status_code == 403


class TestDeleteTask:
    URL: str = '/v1/tasks/{}'

    async def test_success(self, task: Task, client: AsyncClient, auth_headers):
        response = await client.delete(
            self.URL.format(str(task.id)), headers=auth_headers
        )

        assert response.status_code == 204

    async def test_not_found(self, client: AsyncClient, auth_headers):
        response = await client.delete(
            self.URL.format(str(uuid4())), headers=auth_headers
        )

        assert response.status_code == 404

    async def test_not_owned(
        self,
        task: Task,
        client: AsyncClient,
        second_auth_headers
    ):
        response = await client.delete(
            self.URL.format(str(task.id)), headers=second_auth_headers
        )

        assert response.status_code == 403
