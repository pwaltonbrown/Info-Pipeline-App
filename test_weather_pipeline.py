import unittest
from unittest.mock import patch, Mock

import weather_pipeline


class WeatherPipelineTests(unittest.TestCase):
    @patch("weather_pipeline.os.path.exists", return_value=False)
    @patch("pandas.DataFrame.to_csv")
    @patch("weather_pipeline.requests.get")
    def test_run_pipeline_builds_request_with_base_url_and_params(self, mock_get, _mock_to_csv, _mock_exists):
        mock_response = Mock(status_code=200)
        mock_response.json.return_value = {
            "name": "Raleigh",
            "main": {"temp": 75, "humidity": 40},
            "weather": [{"description": "clear sky"}],
        }
        mock_get.return_value = mock_response

        weather_pipeline.run_pipeline()

        mock_get.assert_called_once_with(
            weather_pipeline.BASE_URL,
            params={
                "q": weather_pipeline.CITY,
                "appid": weather_pipeline.API_KEY,
                "units": "imperial",
            },
        )

    @patch("weather_pipeline.os.path.exists", return_value=False)
    @patch("pandas.DataFrame.to_csv")
    @patch("weather_pipeline.requests.get")
    def test_run_pipeline_returns_early_on_failed_api_response(self, mock_get, mock_to_csv, _mock_exists):
        mock_get.return_value = Mock(status_code=500, text="server error")

        weather_pipeline.run_pipeline()

        mock_to_csv.assert_not_called()


if __name__ == "__main__":
    unittest.main()
