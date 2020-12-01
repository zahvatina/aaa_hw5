import unittest
import urllib.request
import json
from unittest.mock import MagicMock, patch

url_mock = MagicMock()
read_mock_defis = MagicMock(return_value={'currentDateTime': '2043-03-01'})
read_mock_tochka = MagicMock(return_value={'currentDateTime': '01.03.2019'})
read_mock_error = MagicMock(return_value={'currentDateTime': '01|03|2019'})

API_URL = 'http://worldclockapi.com/api/json/utc/now'

YMD_SEP = '-'
YMD_SEP_INDEX = 4
YMD_YEAR_SLICE = slice(None, YMD_SEP_INDEX)

DMY_SEP = '.'
DMY_SEP_INDEX = 5
DMY_YEAR_SLICE = slice(DMY_SEP_INDEX + 1, DMY_SEP_INDEX + 5)


def what_is_year_now() -> int:
    """
    Получает текущее время из API-worldclock и извлекает из
     поля 'currentDateTime' год
    Предположим, что currentDateTime может быть в двух форматах:
      * YYYY-MM-DD - 2019-03-01
      * DD.MM.YYYY - 01.03.2019
    """
    with urllib.request.urlopen(API_URL) as resp:
        resp_json = json.load(resp)

    datetime_str = resp_json['currentDateTime']
    if datetime_str[YMD_SEP_INDEX] == YMD_SEP:
        year_str = datetime_str[YMD_YEAR_SLICE]
    elif datetime_str[DMY_SEP_INDEX] == DMY_SEP:
        year_str = datetime_str[DMY_YEAR_SLICE]
    else:
        raise ValueError('Invalid format')

    return int(year_str)


class TestYEAR(unittest.TestCase):
    @patch('urllib.request.urlopen', url_mock)
    @patch('json.load', read_mock_defis)
    def test_year_defis(self):
        year = what_is_year_now()
        expected = 2043

        self.assertEqual(year, expected)

    @patch('urllib.request.urlopen', url_mock)
    @patch('json.load', read_mock_tochka)
    def test_year_tochka(self):
        year = what_is_year_now()
        expected = 2019

        self.assertEqual(year, expected)

    @patch('urllib.request.urlopen', url_mock)
    @patch('json.load', read_mock_error)
    def test_year_error(self):
        with self.assertRaises(ValueError):
            _ = what_is_year_now()
