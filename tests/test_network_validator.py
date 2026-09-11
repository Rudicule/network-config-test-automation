from pathlib import Path
import subprocess

import pytest


PROJECT_ROOT = Path(__file__).resolve().parent.parent
VALIDATOR = PROJECT_ROOT / "network_validator.exe"
TEST_DATA = PROJECT_ROOT / "test_data"


@pytest.fixture
def run_validator():
    if not VALIDATOR.exists():
        pytest.fail(
            f"Validator executable not found: {VALIDATOR}"
        )

    def _run(config_file):
        config_path = TEST_DATA / config_file

        return subprocess.run(
            [str(VALIDATOR), str(config_path)],
            capture_output=True,
            text=True
        )

    return _run


@pytest.mark.parametrize(
    "config_file, expected_output, expected_code",
    [
        pytest.param(
            "valid_config.txt",
            "VALID",
            0,
            id="TC01_valid_configuration"
        ),
        pytest.param(
            "invalid_ip.txt",
            "INVALID",
            2,
            id="TC02_invalid_ipv4"
        ),
        pytest.param(
            "port_zero.txt",
            "INVALID",
            2,
            id="TC03_port_below_minimum"
        ),
        pytest.param(
            "port_min.txt",
            "VALID",
            0,
            id="TC04_port_minimum"
        ),
        pytest.param(
            "port_max.txt",
            "VALID",
            0,
            id="TC05_port_maximum"
        ),
        pytest.param(
            "port_over_max.txt",
            "INVALID",
            2,
            id="TC06_port_above_maximum"
        ),
        pytest.param(
            "invalid_protocol.txt",
            "INVALID",
            2,
            id="TC07_invalid_protocol"
        ),
        pytest.param(
            "http_config.txt",
            "VALID",
            0,
            id="TC08_http_protocol"
        ),
        pytest.param(
            "valid_config.txt",
            "VALID",
            0,
            id="TC09_https_protocol"
        ),
        pytest.param(
            "timeout_zero.txt",
            "INVALID",
            2,
            id="TC10_timeout_below_minimum"
        ),
        pytest.param(
            "timeout_min.txt",
            "VALID",
            0,
            id="TC11_timeout_minimum"
        ),
        pytest.param(
            "timeout_max.txt",
            "VALID",
            0,
            id="TC12_timeout_maximum"
        ),
        pytest.param(
            "timeout_over_max.txt",
            "INVALID",
            2,
            id="TC13_timeout_above_maximum"
        ),
        pytest.param(
            "missing_server.txt",
            "INVALID",
            2,
            id="TC14_missing_server"
        ),
        pytest.param(
            "missing_port.txt",
            "INVALID",
            2,
            id="TC15_missing_port"
        ),
        pytest.param(
            "missing_protocol.txt",
            "INVALID",
            2,
            id="TC16_missing_protocol"
        ),
        pytest.param(
            "missing_timeout.txt",
            "INVALID",
            2,
            id="TC17_missing_timeout"
        ),
        pytest.param(
            "valid_config.txt",
            "VALID",
            0,
            id="TC18_complete_valid_configuration"
        ),
        pytest.param(
            "invalid_config.txt",
            "INVALID",
            2,
            id="TC19_multiple_invalid_fields"
        ),
        pytest.param(
            "empty_config.txt",
            "INVALID",
            2,
            id="TC20_empty_configuration"
        ),
        pytest.param(
            "invalid_port.txt",
            "INVALID",
            2,
            id="TC21_non_numeric_port"
        ),
        pytest.param(
            "invalid_timeout.txt",
            "INVALID",
            2,
            id="TC22_non_numeric_timeout"
        ),
        pytest.param(
            "malformed_ip.txt",
            "INVALID",
            2,
            id="TC23_malformed_ipv4"
        ),
        pytest.param(
            "malformed_config.txt",
            "VALID",
            0,
            id="TC24_malformed_line_ignored"
        ),
    ]
)
def test_configuration(
    run_validator,
    config_file,
    expected_output,
    expected_code
):
    result = run_validator(config_file)

    assert result.stdout.strip() == expected_output
    assert result.returncode == expected_code