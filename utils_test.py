from utils import log
import json
from datetime import datetime


def test_log_txt():
    data = "test log text"
    timestamp_str = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    log(data)

    expected_file_name = f"./output/{timestamp_str}.txt"

    with open(expected_file_name, "r") as f:
        content = f.read()

    assert content == data


def test_log_txt_with_suffix():
    data = "test log text"
    timestamp_str = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    log(data, suffix="test-suffix")

    expected_file_name = f"./output/{timestamp_str}_test-suffix.txt"

    with open(expected_file_name, "r") as f:
        content = f.read()

    assert content == data


def test_log_json():
    data = {"field": "test field"}
    timestamp_str = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    log(data, file_type="json")

    expected_file_name = f"./output/{timestamp_str}.json"

    with open(expected_file_name, "r") as f:
        content = json.load(f)

    print(content)

    assert content == data


def test_log_json_with_suffix():
    data = {"field": "test field"}
    timestamp_str = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    log(data, file_type="json", suffix="test-results")

    expected_file_name = f"./output/{timestamp_str}_test-results.json"

    with open(expected_file_name, "r") as f:
        content = json.load(f)

    print(content)

    assert content == data
