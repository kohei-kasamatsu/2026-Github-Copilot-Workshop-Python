import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app import create_app


class TestCreateApp(unittest.TestCase):
    def test_loads_expected_config_from_app_config(self) -> None:
        app = create_app()

        self.assertEqual(app.config["APP_TITLE"], "Pomodoro Timer")
        self.assertEqual(app.config["WORK_DURATION_MINUTES"], 25)
        self.assertEqual(app.config["SHORT_BREAK_MINUTES"], 5)
        self.assertEqual(app.config["LONG_BREAK_MINUTES"], 15)
        self.assertEqual(app.config["LONG_BREAK_INTERVAL"], 4)

    def test_index_route_returns_html_with_initial_settings(self) -> None:
        app = create_app()
        client = app.test_client()

        response = client.get("/")
        body = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("<title>Pomodoro Timer</title>", body)
        self.assertIn('id="initial-settings"', body)
        self.assertIn('"workDurationMinutes": 25', body)
        self.assertIn('"shortBreakMinutes": 5', body)
        self.assertIn('"longBreakMinutes": 15', body)
        self.assertIn('"longBreakInterval": 4', body)


if __name__ == "__main__":
    unittest.main()