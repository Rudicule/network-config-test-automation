# Network Configuration Test Automation

A QA automation project that validates network configuration files using a C++ command-line application and an automated Python/pytest test suite.

The project demonstrates requirements-driven testing, positive and negative testing, boundary value analysis, data-driven automation, test reporting, and CI execution using GitHub Actions.

## Project Overview

The Application Under Test (AUT) is a C++ command-line Network Configuration Validator.

It reads a configuration file and validates:

- Server IPv4 address
- Port number
- Network protocol
- Connection timeout
- Required configuration fields

The application returns:

- `VALID` with exit code `0` for valid configurations
- `INVALID` with exit code `2` for invalid configurations

Python/pytest is used to automatically execute the test cases against the C++ application.

## Architecture

```text
Configuration File
        |
        v
C++ Network Configuration Validator
        |
        v
Application Output + Exit Code
        |
        v
Python + pytest Automation
        |
        v
24 Automated Test Cases
        |
        v
JUnit XML Test Report
        |
        v
GitHub Actions CI
```

## Requirements

The validator checks the following requirements:

| ID | Requirement |
| --- | --- |
| R1 | Server must be a valid IPv4 address |
| R2 | Port must be between 1 and 65535 |
| R3 | Protocol must be `http` or `https` |
| R4 | Timeout must be between 1 and 300 seconds |
| R5 | Server, port, protocol and timeout are required fields |

## Test Strategy

The automated test suite contains 24 test cases covering:

### Positive Testing

Valid inputs are used to verify that the application accepts correct configurations.

Examples:

- Minimum valid port: `1`
- Maximum valid port: `65535`
- Minimum valid timeout: `1`
- Maximum valid timeout: `300`
- Valid `http` configuration
- Valid `https` configuration

### Negative Testing

Invalid inputs are used to verify that the application rejects incorrect configurations.

Examples:

- Invalid IPv4 address
- Port below minimum
- Port above maximum
- Invalid protocol
- Timeout outside the allowed range
- Missing required fields
- Non-numeric port and timeout values
- Malformed IPv4 address

### Boundary Value Analysis

Boundary values are specifically tested because defects frequently occur at the edges of allowed ranges.

For example:

Port:

0       -> INVALID
1       -> VALID
65535   -> VALID
65536   -> INVALID

Timeout:

0       -> INVALID
1       -> VALID
300     -> VALID
301     -> INVALID

### Equivalence Partitioning

Inputs are divided into valid and invalid equivalence classes.

Representative values from each class are used to reduce unnecessary duplication while maintaining useful coverage.

## Test Automation

The test suite is implemented using Python and pytest.

The tests use:

- pytest fixtures
- parameterized testing
- test case IDs
- subprocess execution
- assertions
- filesystem path handling
- exit-code validation
- stdout validation

The test cases are data-driven using `pytest.mark.parametrize`.

Each automated test verifies both:

1. Application output
2. Application exit code

Example:

Expected output: `VALID`

Expected exit code: `0`

## Test Case Traceability

The automated tests use IDs such as:

- `TC01_valid_configuration`
- `TC02_invalid_ipv4`
- `TC03_port_below_minimum`
- `TC04_port_minimum`
- `TC05_port_maximum`
- `TC06_port_above_maximum`
- ...
- `TC24_malformed_line_ignored`

This provides traceability between the requirements, manual test cases and automated tests.

The complete test case specification is available in:

`tests/test_cases.md`

## Continuous Integration

GitHub Actions is used to automatically build and test the project.

The CI pipeline:

1. Checks out the repository
2. Sets up Python
3. Installs pytest
4. Compiles the C++ application
5. Runs the automated test suite
6. Generates a JUnit XML test report
7. Uploads the test report as a GitHub Actions artifact

The pipeline runs on:

- Pushes to the repository
- Pull requests

## Test Results

Current automated test result:

`24 passed`

Example local execution:

`python -m pytest -v --junitxml=reports/test-results.xml`

Example result:

`24 passed`

`- generated xml file: reports/test-results.xml -`

## Project Structure

```text
network-config-test-automation/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── reports/
│
├── src/
│   └── network_validator.cpp
│
├── test_data/
│   ├── valid_config.txt
│   ├── invalid_ip.txt
│   ├── port_zero.txt
│   ├── port_min.txt
│   ├── port_max.txt
│   ├── port_over_max.txt
│   └── ...
│
├── tests/
│   ├── test_cases.md
│   └── test_network_validator.py
│
├── .gitignore
└── README.md
```

## Running Locally

### 1. Compile the C++ application

Using a C++ compiler:

`g++ src/network_validator.cpp -o network_validator.exe -static`

### 2. Run the validator manually

`.\network_validator.exe test_data\valid_config.txt`

Expected output:

`VALID`

### 3. Run the automated tests

`python -m pytest -v`

### 4. Generate a test report

`python -m pytest -v --junitxml=reports/test-results.xml`

## QA Findings

During development, the project also involved environment and execution troubleshooting.

The C++ executable initially depended on runtime DLLs provided by the MSYS2 environment. When the executable was launched from PowerShell through pytest, it failed to execute correctly.

The dependency issue was diagnosed using:

`ldd network_validator.exe`

The application was then rebuilt using static linking:

`g++ src/network_validator.cpp -o network_validator.exe -static`

This allowed the executable to run correctly from the pytest environment and CI workflow.

This demonstrates a practical QA debugging workflow:

```text
Test Failure
     |
     v
Investigate Error
     |
     v
Check Runtime Dependencies
     |
     v
Identify Root Cause
     |
     v
Apply Fix
     |
     v
Re-run Automated Tests
```

## Known Behavior

Configuration lines without an `=` delimiter are currently ignored by the application.

For example:

`THIS_IS_NOT_VALID`

is ignored while valid required fields are still processed.

This behavior is explicitly represented by `TC24_malformed_line_ignored`.

## Technologies Used

- C++
- Python
- pytest
- Git
- GitHub
- GitHub Actions
- Windows
- MSYS2
- JUnit XML test reporting

## Key QA Concepts Demonstrated

- Requirements-driven testing
- Positive testing
- Negative testing
- Boundary Value Analysis
- Equivalence Partitioning
- Data-driven testing
- Test case traceability
- Automated regression testing
- Application Under Test (AUT)
- Exit-code validation
- CI/CD testing
- Test reporting
- Environment troubleshooting

## Resume Project Summary

Network Configuration Test Automation | C++, Python, pytest, GitHub Actions

Developed a C++ network configuration validator and automated 24 requirements-driven test cases using Python/pytest, covering positive, negative, boundary-value and missing-field scenarios. Implemented data-driven testing, test fixtures, exit-code/output validation, JUnit XML reporting and GitHub Actions CI for automated build and regression testing.