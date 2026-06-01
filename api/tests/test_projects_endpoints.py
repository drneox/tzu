"""
Tests for project CRUD endpoints
"""
import pytest
import uuid
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _create_project(client, headers, name="TestProject", description=None):
    payload = {"name": name}
    if description:
        payload["description"] = description
    return client.post("/projects", json=payload, headers=headers)


# ===========================================================================
# LIST PROJECTS
# ===========================================================================

class TestListProjects:
    def test_list_requires_auth(self, test_client):
        resp = test_client.get("/projects")
        assert resp.status_code == 401

    def test_list_returns_empty_initially(self, test_client, auth_headers):
        resp = test_client.get("/projects", headers=auth_headers)
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)

    def test_list_returns_created_projects(self, test_client, analyst_auth_headers, auth_headers):
        _create_project(test_client, analyst_auth_headers, name=f"P-{uuid.uuid4().hex[:8]}")
        resp = test_client.get("/projects", headers=auth_headers)
        assert resp.status_code == 200
        assert len(resp.json()) >= 1


# ===========================================================================
# CREATE PROJECT
# ===========================================================================

class TestCreateProject:
    def test_create_requires_auth(self, test_client):
        resp = test_client.post("/projects", json={"name": "X"})
        assert resp.status_code == 401

    def test_create_requires_analyst(self, test_client, auth_headers):
        """Regular (viewer) user should not be able to create"""
        resp = _create_project(test_client, auth_headers, name="ShouldFail")
        # viewer role → 403
        assert resp.status_code == 403

    def test_create_as_analyst(self, test_client, analyst_auth_headers):
        name = f"Proj-{uuid.uuid4().hex[:8]}"
        resp = _create_project(test_client, analyst_auth_headers, name=name)
        assert resp.status_code == 201
        data = resp.json()
        assert data["name"] == name
        assert "id" in data
        assert "created_at" in data

    def test_create_with_description(self, test_client, analyst_auth_headers):
        resp = _create_project(test_client, analyst_auth_headers, name=f"PD-{uuid.uuid4().hex[:6]}", description="My desc")
        assert resp.status_code == 201
        assert resp.json()["description"] == "My desc"

    def test_create_empty_name_rejected(self, test_client, analyst_auth_headers):
        resp = test_client.post("/projects", json={"name": "   "}, headers=analyst_auth_headers)
        assert resp.status_code == 400

    def test_create_as_admin(self, test_client, admin_auth_headers):
        resp = _create_project(test_client, admin_auth_headers, name=f"Admin-{uuid.uuid4().hex[:6]}")
        assert resp.status_code == 201


# ===========================================================================
# GET PROJECT
# ===========================================================================

class TestGetProject:
    def test_get_requires_auth(self, test_client, analyst_auth_headers):
        resp = _create_project(test_client, analyst_auth_headers, name=f"G-{uuid.uuid4().hex[:6]}")
        pid = resp.json()["id"]
        resp2 = test_client.get(f"/projects/{pid}")
        assert resp2.status_code == 401

    def test_get_existing(self, test_client, analyst_auth_headers, auth_headers):
        name = f"GetMe-{uuid.uuid4().hex[:6]}"
        resp = _create_project(test_client, analyst_auth_headers, name=name)
        pid = resp.json()["id"]
        resp2 = test_client.get(f"/projects/{pid}", headers=auth_headers)
        assert resp2.status_code == 200
        assert resp2.json()["name"] == name

    def test_get_nonexistent_returns_404(self, test_client, auth_headers):
        fake_id = str(uuid.uuid4())
        resp = test_client.get(f"/projects/{fake_id}", headers=auth_headers)
        assert resp.status_code == 404

    def test_get_returns_counts(self, test_client, analyst_auth_headers, auth_headers):
        resp = _create_project(test_client, analyst_auth_headers, name=f"Cnt-{uuid.uuid4().hex[:6]}")
        pid = resp.json()["id"]
        resp2 = test_client.get(f"/projects/{pid}", headers=auth_headers)
        data = resp2.json()
        assert "analysis_count" in data
        assert "member_count" in data
        assert data["analysis_count"] == 0
        assert data["member_count"] == 0


# ===========================================================================
# UPDATE PROJECT
# ===========================================================================

class TestUpdateProject:
    def test_update_as_owner(self, test_client, analyst_auth_headers):
        resp = _create_project(test_client, analyst_auth_headers, name=f"OldName-{uuid.uuid4().hex[:6]}")
        pid = resp.json()["id"]
        resp2 = test_client.put(f"/projects/{pid}", json={"name": "NewName"}, headers=analyst_auth_headers)
        assert resp2.status_code == 200
        assert resp2.json()["name"] == "NewName"

    def test_update_as_non_owner_forbidden(self, test_client, analyst_auth_headers, auth_headers):
        resp = _create_project(test_client, analyst_auth_headers, name=f"Own-{uuid.uuid4().hex[:6]}")
        pid = resp.json()["id"]
        resp2 = test_client.put(f"/projects/{pid}", json={"name": "Hacked"}, headers=auth_headers)
        assert resp2.status_code == 403

    def test_update_as_admin(self, test_client, analyst_auth_headers, admin_auth_headers):
        resp = _create_project(test_client, analyst_auth_headers, name=f"ForAdmin-{uuid.uuid4().hex[:6]}")
        pid = resp.json()["id"]
        resp2 = test_client.put(f"/projects/{pid}", json={"name": "AdminUpdated"}, headers=admin_auth_headers)
        assert resp2.status_code == 200

    def test_update_nonexistent_returns_404(self, test_client, analyst_auth_headers):
        fake_id = str(uuid.uuid4())
        resp = test_client.put(f"/projects/{fake_id}", json={"name": "X"}, headers=analyst_auth_headers)
        assert resp.status_code == 404


# ===========================================================================
# DELETE PROJECT
# ===========================================================================

class TestDeleteProject:
    def test_delete_as_owner(self, test_client, analyst_auth_headers):
        resp = _create_project(test_client, analyst_auth_headers, name=f"Del-{uuid.uuid4().hex[:6]}")
        pid = resp.json()["id"]
        resp2 = test_client.delete(f"/projects/{pid}", headers=analyst_auth_headers)
        assert resp2.status_code == 204

    def test_delete_as_non_owner_forbidden(self, test_client, analyst_auth_headers, auth_headers):
        resp = _create_project(test_client, analyst_auth_headers, name=f"NDel-{uuid.uuid4().hex[:6]}")
        pid = resp.json()["id"]
        resp2 = test_client.delete(f"/projects/{pid}", headers=auth_headers)
        assert resp2.status_code == 403

    def test_delete_as_admin(self, test_client, analyst_auth_headers, admin_auth_headers):
        resp = _create_project(test_client, analyst_auth_headers, name=f"ADel-{uuid.uuid4().hex[:6]}")
        pid = resp.json()["id"]
        resp2 = test_client.delete(f"/projects/{pid}", headers=admin_auth_headers)
        assert resp2.status_code == 204

    def test_delete_nonexistent_returns_404(self, test_client, analyst_auth_headers):
        fake_id = str(uuid.uuid4())
        resp = test_client.delete(f"/projects/{fake_id}", headers=analyst_auth_headers)
        assert resp.status_code == 404

    def test_after_delete_get_returns_404(self, test_client, analyst_auth_headers, auth_headers):
        resp = _create_project(test_client, analyst_auth_headers, name=f"Gone-{uuid.uuid4().hex[:6]}")
        pid = resp.json()["id"]
        test_client.delete(f"/projects/{pid}", headers=analyst_auth_headers)
        resp2 = test_client.get(f"/projects/{pid}", headers=auth_headers)
        assert resp2.status_code == 404
