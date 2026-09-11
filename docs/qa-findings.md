# QA Findings and Investigation

This document records issues and observations identified during development and testing of the Network Configuration Test Automation project.

## 1. C++ Runtime Dependency Issue

### Description

The C++ application initially compiled successfully and ran correctly when executed directly from the MSYS2 UCRT64 environment.

However, when the executable was launched from PowerShell through the Python/pytest automation framework, the automated test failed.

The failure produced the following return code:

```text
3221225781
```

### Investigation

The executable's runtime dependencies were inspected using:

```bash
ldd network_validator.exe
```

The output showed dependencies on MSYS2 runtime libraries, including:

- `libgcc_s_seh-1.dll`
- `libstdc++-6.dll`
- `libwinpthread-1.dll`

This indicated that the executable depended on runtime libraries that were not available in the PowerShell execution environment used by pytest.

### Root Cause

The application was dynamically linked against MSYS2 runtime libraries.

The manual execution environment and the pytest execution environment therefore did not have identical runtime dependencies.

### Resolution

The application was rebuilt using static linking:

```bash
g++ src/network_validator.cpp -o network_validator.exe -static
```

The executable was then checked again using:

```bash
ldd network_validator.exe
```

The MSYS2 runtime dependencies were no longer required.

The pytest suite was then executed successfully.

### Verification

After the fix:

```text
24 passed
```

The same build approach is also used by the GitHub Actions CI workflow.

### QA Lesson

A test failure does not necessarily indicate a defect in the application logic.

The failure can originate from the test environment, runtime dependencies, configuration, or execution method.

The investigation followed this process:

```text
Test Failure
     |
     v
Investigate Failure
     |
     v
Inspect Runtime Dependencies
     |
     v
Identify Root Cause
     |
     v
Apply Fix
     |
     v
Re-run Tests
     |
     v
Verify Successful Execution
```

---

## 2. Malformed Configuration Line Behavior

### Observation

The application currently ignores configuration lines that do not contain an `=` delimiter.

For example:

```text
THIS_IS_NOT_VALID
```

is ignored by the parser.

If all required configuration fields are otherwise valid, the application still returns:

```text
VALID
```

with exit code:

```text
0
```

### Test Coverage

This behavior is explicitly tested by:

```text
TC24_malformed_line_ignored
```

The test verifies the current expected behavior rather than treating the malformed line as an application failure.

### QA Consideration

Whether malformed lines should be ignored or rejected is a requirements decision.

If future requirements specify that every configuration line must follow the `key=value` format, a new negative test should be introduced and the application behavior should be updated accordingly.

---

## 3. Testing Approach

The project uses multiple test design techniques to improve coverage.

### Positive Testing

Valid configurations are tested to confirm that expected inputs are accepted.

### Negative Testing

Invalid configurations are tested to confirm that invalid inputs are rejected.

### Boundary Value Analysis

Values at and immediately outside defined boundaries are tested.

Examples:

```text
Port:
0       -> INVALID
1       -> VALID
65535   -> VALID
65536   -> INVALID
```

```text
Timeout:
0       -> INVALID
1       -> VALID
300     -> VALID
301     -> INVALID
```

### Equivalence Partitioning

Inputs are grouped into valid and invalid classes, with representative values selected for testing.

### Requirements Traceability

The requirements are mapped to test cases and then to automated pytest tests.

---

## 4. Future Test Enhancements

The current suite contains 24 automated tests.

Potential future improvements include:

- Additional malformed configuration cases
- Additional IPv4 edge cases
- Duplicate configuration keys
- Empty field values
- Whitespace handling
- Additional invalid numeric formats
- More extensive parser validation
- Code coverage measurement
- Additional CI environments

These are considered future enhancements rather than current defects because the current project requirements do not define expected behavior for all of these cases.