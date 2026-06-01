"""
Tests for project members endpoints
"""
import pytest
import uuid
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _create_project(client, headers, name=None):
    name = name or f"MP-{uuid.uuid4().hex[:8]}"
    resp = client.post("/projects", json={"name": name}, headers=headers)
    assert resp.status_code == 201
    return resp.json()


# ===========================================================================
# LIST MEMBERS
# ===========================================================================

class TestListMembers:
    def test_list_requires_auth(self, test_client, analyst_auth_headers):
        proj = _create_project(test_client, analyst_auth_headers)
        resp = test_client.get(f"/projects/{proj['id']}/members")
        assert resp.status_code == 401

    def test_list_empty_initially(self, test_client, analyst_auth_headers):
        proj = _create_project(test_client, analyst_auth_headers)
        resp = test_client.get(f"/projects/{proj['id']}/members", headers=analyst_auth_headers)
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)

    def test_list_non_owner_forbidden(self, test_client, analyst_auth_headers, auth_headers):
        proj = _create_project(test_client, analyst_auth_headers)
        resp = test_client.get(f"/projects/{proj['id']}/members", headers=auth_headers)
        assert resp.status_code == 403

    def test_list_nonexistent_project(self, test_client, analyst_auth_headers):
        fake_id = str(uuid.uuid4())
        resp = test_client.get(f"/projects/{fake_id}/members", headers=analyst_auth_headers)
        assert resp.status_code == 404


# ===========================================================================
# ADD MEMBER
# ===========================================================================

class TestAddMember:
    def test_add_requires_auth(self, test_client, analyst_auth_headers):
        proj = _create_project(test_client, analyst_auth_headers)
        resp = test_client.post(f"/projects/{proj['id']}/members", json={"user_id": str(uuid.uuid4())})
        assert resp.status_code == 401

    def test_add_non_owner_forbidden(self, test_client, analyst_auth_headers, auth_headers, test_user):
        proj = _create_project(test_client, analyst_auth_headers)
        resp = test_client.post(
            f"/projects/{proj['id']}/members",
            json={"user_id": str(test_user.id)},
            headers=auth_headers,
        )
        assert resp.status_code == 403

    def test_add_nonexistent_user(self, test_client, analyst_auth_headers):
        proj = _create_project(test_client, analyst_auth_headers)
        fake_uid = str(uuid.uuid4())
        resp = test_client.post(
            f"/projects/{proj['id']}/members",
            json={"user_id": fake_uid},
            headers=analyst_auth_headers,
        )
        assert resp.status_code == 400

    def test_add_existing_user_as_owner(self, test_client, analyst_auth_headers, test_user):
        proj = _create_project(test_client, analyst_auth_headers)
        resp = test_client.post(
            f"/projects/{proj['id']}/members",
            json={"user_id": str(test_user.id)},
            headers=analyst_auth_headers,
        )
        assert resp.status_code == 201
        data = resp.json()
        assert str(data["user_id"]) == str(test_user.id)
        assert "username" in data
        assert "added_at" in data

    def test_add_same_user_twice_409(self, test_client, analyst_auth_headers, test_user):
        proj = _create_project(test_client, analyst_auth_headers)
        test_client.post(
            f"/projects/{proj['id']}/members",
            json={"user_id": str(test_user.id)},
            headers=analyst_auth_headers,
        )
        resp = test_client.post(
            f"/projects/{proj['id']}/members",
            json={"user_id": str(test_user.id)},
            headers=analyst_auth_headers,
        )
        assert resp.status_code == 409

    def test_admin_can_add_member(self, test_client, analyst_auth_headers, admin_auth_headers, test_user):
        proj = _create_project(test_client, analyst_auth_headers)
        resp = test_client.post(
            f"/projects/{proj['id']}/members",
            json={"user_id": str(test_user.id)},
            headers=admin_auth_headers,
        )
        assert resp.status_code == 201


# ===========================================================================
# REMOVE MEMBER
# ===========================================================================

class TestRemoveMember:
    def test_remove_as_owner(self, test_client, analyst_auth_headers, test_user):
        proj = _create_project(test_client, analyst_auth_headers)
        # Add member first
        test_client.post(
            f"/projects/{proj['id']}/members",
            json={"user_id": str(test_user.id)},
            headers=analyst_auth_headers,
        )
        resp = test_client.delete(
            f"/projects/{proj['id']}/members/{test_user.id}",
            headers=analyst_auth_headers,
        )
        assert resp.status_code == 204

    def test_remove_non_owner_forbidden(self, test_client, analyst_auth_headers, auth_headers, test_user):
        proj = _create_project(test_client, analyst_auth_headers)
        test_client.post(
            f"/projects/{proj['id']}/members",
            json={"user_id": str(test_user.id)},
            headers=analyst_auth_headers,
        )
        resp = test_client.delete(
            f"/projects/{proj['id']}/members/{test_user.id}",
            headers=auth_headers,
        )
        assert resp.status_code == 403

    def test_remove_nonexistent_returns_404(self, test_client, analyst_auth_headers, test_user):
        proj = _create_project(test_client, analyst_auth_headers)
        fake_uid = str(uuid.uuid4())
        resp = test_client.delete(
            f"/projects/{proj['id']}/members/{fake_uid}",
            headers=analyst_auth_headers,
        )
        assert resp.status_code == 404

    def test_admin_can_remove_member(self, test_client, analyst_auth_headers, admin_auth_headers, test_user):
        proj = _create_project(test_client, analyst_auth_headers)
        test_client.post(
            f"/projects/{proj['id']}/members",
            json={"user_id": str(test_user.id)},
            headers=analyst_auth_headers,
        )
        resp = test_client.delete(
            f"/projects/{proj['id']}/members/{test_user.id}",
            headers=admin_auth_headers,
        )
        assert resp.status_code == 204

    def test_member_count_updates(self, test_client, analyst_auth_headers, auth_headers, test_user):
        proj = _create_project(test_client, analyst_auth_headers)
        pid = proj["id"]

        # Add
        test_client.post(
            f"/projects/{pid}/members",
            json={"user_id": str(test_user.id)},
            headers=analyst_auth_headers,
        )
        resp = test_client.get(f"/projects/{pid}", headers=auth_headers)
        assert resp.json()["member_count"] == 1

        # Remove
        test_client.delete(f"/projects/{pid}/members/{test_user.id}", headers=analyst_auth_headers)
        resp2 = test_client.get(f"/projects/{pid}", headers=auth_headers)
        assert resp2.json()["member_count"] == 0
