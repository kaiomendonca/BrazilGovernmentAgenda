from app.services.request_service import request_data
from pytest_mock import MockerFixture
import requests


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
        
        
    def test_request_data_returns_none_on_error(self, mocker: MockerFixture):
        request_error = requests.exceptions.RequestException
        
        mocker.patch(
            "app.services.request_service.requests.get",
            side_effect=request_error
        )
        
        result = request_data("http://fake-url")
        
        assert result is None
        