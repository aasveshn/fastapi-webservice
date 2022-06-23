from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_image_1():
    response = client.get("/frames/8")
    assert response.status_code == 200
    assert response.json() == {
        "id": 8,
        "name": "558f997a-acf2-4ad4-bc41-6c287154fa36",
         "registration_date": "2022-06-23T20:30:28.451510"
    }

def test_get_image_2():
    response = client.get("/frames/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "23e42bda-0a3e-4402-8a8e-757b544d5030",
         "registration_date": "2022-06-23T20:30:27.458454"
    }

def test_upload_image_fail_1():

    List_t=[]
    response = client.post("/frames/",List_t)
    assert response.status_code == 422


def test_upload_image_fail_2():
    with open("example.jpg", "rb") as f:
        response = client.post("/", files={"file": ("filename", f, "image/jpeg")})
    assert response.status_code == 404












