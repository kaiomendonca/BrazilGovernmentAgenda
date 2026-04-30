from app.utils.date_utils import generate_dates


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
            