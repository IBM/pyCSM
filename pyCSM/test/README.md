# pyCSM Test Suite

This directory contains the test suite for the pyCSM Python client library. The tests verify the functionality of the CSM RESTful API client implementations.

## Test Structure

The test suite is organized into the following test modules:

- **test_session_service.py** - Tests for session management operations
- **test_copyset_service.py** - Tests for copyset operations
- **test_schedule_service.py** - Tests for schedule management
- **test_hardware_service.py** - Tests for hardware service operations
- **test_system_service.py** - Tests for system service operations

## Prerequisites

### Python Version
- Python 3.10 or higher

### Dependencies
Install the test dependencies using pip:

```bash
pip install -r requirements.txt
```

Alternatively, install the main project dependencies first:
```bash
pip install -r ../requirements.txt
pip install -r requirements.txt
```

## Running the Tests

### Run All Tests

From the project root directory (`pyCSM/`):

```bash
python -m unittest discover -s pyCSM/test -p "test_*.py"
```

Or from the test directory:

```bash
cd pyCSM/test
python -m unittest discover -p "test_*.py"
```

### Run a Specific Test Module

```bash
python -m unittest pyCSM.test.test_session_service
```

Or:

```bash
python -m unittest pyCSM.test.test_hardware_service
```

### Run a Specific Test Class

```bash
python -m unittest pyCSM.test.test_session_service.TestSessionService
```

### Run a Specific Test Method

```bash
python -m unittest pyCSM.test.test_session_service.TestSessionService.test_create_session_success
```

### Run Tests with Verbose Output

Add the `-v` flag for verbose output:

```bash
python -m unittest discover -s pyCSM/test -p "test_*.py" -v
```

## Using pytest (Optional)

If you prefer pytest, you can run the tests using:

```bash
# Install pytest if not already installed
pip install pytest pytest-cov

# Run all tests
pytest pyCSM/test/

# Run with coverage report
pytest --cov=pyCSM --cov-report=html pyCSM/test/

# Run a specific test file
pytest pyCSM/test/test_session_service.py

# Run with verbose output
pytest -v pyCSM/test/
```

## Test Coverage

To generate a coverage report using the `coverage` tool:

```bash
# Install coverage if not already installed
pip install coverage

# Run tests with coverage
coverage run -m unittest discover -s pyCSM/test -p "test_*.py"

# Generate coverage report
coverage report

# Generate HTML coverage report
coverage html
```

The HTML report will be generated in the `htmlcov/` directory.

## License

Copyright (C) 2022 IBM CORPORATION  
Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)