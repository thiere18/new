def test_health_check_main(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json().get("status") == "Ok"


def test_godd_file(client, test_superuser, superuser_token_headers):
    files = {"file": open("backend/tests/example/sample.pdf", "rb")}
    url = "/api/highlights"
    response = client.post(url, files=files, headers=superuser_token_headers)
    assert response.status_code == 200


def test_bad_file(client, test_superuser, superuser_token_headers):
    files = {"file": open("backend/tests/example/sample.txt", "rb")}
    url = "/api/highlights"
    response = client.post(url, files=files, headers=superuser_token_headers)
    assert response.status_code == 422
    assert response.json() == {"detail": "This file is not a pdf or it is corrupted"}
