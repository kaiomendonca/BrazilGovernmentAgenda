from app.services.request_service import request_data
from pytest_mock import MockerFixture

class TestRequestData:
    
    def test_request_data_returns_event(self, mocker: MockerFixture):
        mock_response = mocker.Mock()
        
        mock_response.json.return_value =[
            {"isSelected": False, "items": []},
            {"isSelected": True, "items": [{"id": 1}, {"id": 2}]}
        ]
        
        mocker.patch("app.services.request_service.requests.get", return_value =mock_response)
        
        result = request_data("http://fake-url")
        
        assert result == [{"id": 1}, {"id": 2}]
        