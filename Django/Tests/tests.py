import requests

class TestPagesAccessibility:

    def test_whenAccessingAuthorizationPage_statusCodeOk(self):
        response = requests.get("127.0.0.1:8000/admin/")
        assert response.status_code == 200

    def test_whenAccessingInternalPage_statusCodeUnauthorized(self):
        response = requests.get("127.0.0.1:8000/api/v1")
        assert response.status_code == 401
