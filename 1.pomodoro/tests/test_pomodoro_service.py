import unittest
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from services.pomodoro_service import get_initial_settings


class TestGetInitialSettings(unittest.TestCase):
    def test_returns_expected_mapping(self) -> None:
        config = {
            "WORK_DURATION_MINUTES": 30,
            "SHORT_BREAK_MINUTES": 7,
            "LONG_BREAK_MINUTES": 20,
            "LONG_BREAK_INTERVAL": 5,
        }

        settings = get_initial_settings(config)

        self.assertEqual(
            settings,
            {
                "workDurationMinutes": 30,
                "shortBreakMinutes": 7,
                "longBreakMinutes": 20,
                "longBreakInterval": 5,
            },
        )

    def test_raises_key_error_when_config_is_incomplete(self) -> None:
        incomplete_config = {
            "WORK_DURATION_MINUTES": 25,
            "SHORT_BREAK_MINUTES": 5,
            "LONG_BREAK_MINUTES": 15,
        }

        with self.assertRaises(KeyError):
            get_initial_settings(incomplete_config)