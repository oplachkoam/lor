import pytest

from uuid import UUID
from httpx import AsyncClient


@pytest.mark.asyncio
class TestCharacters:
    async def test_create(self, client: AsyncClient):
        response = await client.post(
            "/api/characters",
            json={
                "name": "Фродо Бэггинс",
                "description": "Хоббит из Шира"
            }
        )

        assert response.status_code == 200
        data = response.json()

        assert "id" in data
        assert data["name"] == "Фродо Бэггинс"
        assert data["description"] == "Хоббит из Шира"
        assert "created_at" in data

        UUID(data["id"])

    async def test_create_duplicate_name(self, client: AsyncClient):
        await client.post(
            "/api/characters",
            json={
                "name": "Гэндальф",
                "description": "Серый маг"
            }
        )

        response = await client.post(
            "/api/characters",
            json={
                "name": "Гэндальф",
                "description": "Белый маг"
            }
        )

        assert response.status_code == 409
        assert response.json()["detail"] == "Name already exists"

    async def test_get_by_id(self, client: AsyncClient):
        create_response = await client.post(
            "/api/characters",
            json={
                "name": "Арагорн",
                "description": "Следопыт"
            }
        )

        character_id = create_response.json()["id"]

        response = await client.get(f"/api/characters/{character_id}")

        assert response.status_code == 200
        data = response.json()

        assert data["id"] == character_id
        assert data["name"] == "Арагорн"
        assert data["description"] == "Следопыт"

    async def test_not_found(self, client: AsyncClient):
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = await client.get(f"/api/characters/{fake_id}")

        assert response.status_code == 404
        assert response.json()["detail"] == "Character not found"

    async def test_get_all(self, client: AsyncClient):
        await client.post(
            "/api/characters",
            json={"name": "Фродо", "description": "Хоббит"}
        )
        await client.post(
            "/api/characters",
            json={"name": "Сэм", "description": "Садовник"}
        )
        await client.post(
            "/api/characters",
            json={"name": "Мерри", "description": "Авантюрист"}
        )

        response = await client.get("/api/characters")

        assert response.status_code == 200
        data = response.json()

        assert "characters" in data
        assert len(data["characters"]) == 3

    async def test_update(self, client: AsyncClient):
        create_response = await client.post(
            "/api/characters",
            json={
                "name": "Гимли",
                "description": "Гном"
            }
        )

        character_id = create_response.json()["id"]

        response = await client.put(
            f"/api/characters/{character_id}",
            json={
                "name": "Гимли сын Глоина",
                "description": "Гном, воин Братства Кольца"
            }
        )

        assert response.status_code == 200
        data = response.json()

        assert data["id"] == character_id
        assert data["name"] == "Гимли сын Глоина"
        assert data["description"] == "Гном, воин Братства Кольца"

    async def test_update_not_found(self, client: AsyncClient):
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = await client.put(
            f"/api/characters/{fake_id}",
            json={
                "name": "Тест",
                "description": "Описание"
            }
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "Character not found"

    async def test_delete(self, client: AsyncClient):
        create_response = await client.post(
            "/api/characters",
            json={
                "name": "Боромир",
                "description": "Воин Гондора"
            }
        )

        character_id = create_response.json()["id"]

        response = await client.delete(f"/api/characters/{character_id}")

        assert response.status_code == 200

        get_response = await client.get(f"/api/characters/{character_id}")
        assert get_response.status_code == 404

    async def test_delete_not_found(self, client: AsyncClient):
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = await client.delete(f"/api/characters/{fake_id}")

        assert response.status_code == 404
        assert response.json()["detail"] == "Character not found"
