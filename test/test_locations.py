import pytest

from uuid import UUID
from httpx import AsyncClient


@pytest.mark.asyncio
class TestLocations:
    async def test_create(self, client: AsyncClient):
        char_response = await client.post(
            "/api/characters",
            json={
                "name": "Фродо",
                "description": "Хоббит"
            }
        )

        character_id = char_response.json()["id"]

        response = await client.post(
            "/api/locations",
            json={
                "character_id": character_id,
                "x": 10.5,
                "y": 20.3
            }
        )

        assert response.status_code == 200
        data = response.json()

        assert "id" in data
        assert data["character_id"] == character_id
        assert data["x"] == 10.5
        assert data["y"] == 20.3
        assert "created_at" in data

        UUID(data["id"])

    async def test_create_character_not_found(self, client: AsyncClient):
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = await client.post(
            "/api/locations",
            json={
                "character_id": fake_id,
                "x": 10.5,
                "y": 20.3
            }
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "Character not found"

    async def test_get_by_character_id(self, client: AsyncClient):
        char_response = await client.post(
            "/api/characters",
            json={
                "name": "Арагорн",
                "description": "Следопыт"
            }
        )

        character_id = char_response.json()["id"]

        await client.post(
            "/api/locations",
            json={"character_id": character_id, "x": 1.0, "y": 1.0}
        )
        await client.post(
            "/api/locations",
            json={"character_id": character_id, "x": 2.0, "y": 2.0}
        )
        await client.post(
            "/api/locations",
            json={"character_id": character_id, "x": 3.0, "y": 3.0}
        )

        response = await client.get(f"/api/locations/{character_id}")

        assert response.status_code == 200
        data = response.json()

        assert "locations" in data
        assert len(data["locations"]) == 3

    async def test_get_character_not_found(self, client: AsyncClient):
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = await client.get(f"/api/locations/{fake_id}")

        assert response.status_code == 404
        assert response.json()["detail"] == "Character not found"

    async def test_delete(self, client: AsyncClient):
        char_response = await client.post(
            "/api/characters",
            json={
                "name": "Леголас",
                "description": "Эльф"
            }
        )

        character_id = char_response.json()["id"]

        loc_response = await client.post(
            "/api/locations",
            json={"character_id": character_id, "x": 5.0, "y": 5.0}
        )
        location_id = loc_response.json()["id"]

        response = await client.delete(f"/api/locations/{location_id}")

        assert response.status_code == 200

        get_response = await client.get(f"/api/locations/{character_id}")
        assert len(get_response.json()["locations"]) == 0

    async def test_delete_not_found(self, client: AsyncClient):
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = await client.delete(f"/api/locations/{fake_id}")

        assert response.status_code == 404
        assert response.json()["detail"] == "Location not found"
