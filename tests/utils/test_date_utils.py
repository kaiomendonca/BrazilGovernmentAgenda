from app.utils.date_utils import generate_dates
import pytest
from click import ClickException


class TestGenerateDates:
    
    
    def test_generate_dates(self):
        assert generate_dates("2026-01-04", "2026-01-06") == [
            '2026-01-04',
            '2026-01-05',
            '2026-01-06'
        ]
        
   
    def test_single_day(self):
        assert generate_dates("2026-01-04", "2026-01-04") == [
            "2026-01-04"
        ]
            
            
    def test_generate_dates_invalid_dates(self):
        with pytest.raises(ClickException):
            generate_dates("2026-02-30", "2026-03-05")

    def test_generate_dates_reverse_interval(self):
        with pytest.raises(ClickException):
            generate_dates("2026-04-03", "2026-04-01")
        