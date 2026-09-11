# Network Configuration Validator — Test Cases

## 1. Application Requirements

### R1 — Server Address

The `server` field must contain a valid IPv4 address.

### R2 — Port

The `port` field must contain a value between 1 and 65535.

### R3 — Protocol

The `protocol` field must contain either `http` or `https`.

### R4 — Timeout

The `timeout` field must contain a value between 1 and 300 seconds.

### R5 — Required Fields

The configuration must contain all four required fields:

- server
- port
- protocol
- timeout

---

## 2. Test Cases

| ID | Requirement | Test Scenario | Test Input | Expected Result |
|---|---|---|---|---|
| TC01 | R1 | Valid IPv4 address | 192.168.1.10 | VALID |
| TC02 | R1 | Invalid IPv4 address | 192.168.1.999 | INVALID |
| TC03 | R1 | Incomplete IPv4 address | 192.168.1 | INVALID |
| TC04 | R1 | Non-numeric IPv4 address | abc.def.ghi.jkl | INVALID |
| TC05 | R2 | Minimum valid port | 1 | VALID |
| TC06 | R2 | Below minimum port | 0 | INVALID |
| TC07 | R2 | Normal valid port | 443 | VALID |
| TC08 | R2 | Maximum valid port | 65535 | VALID |
| TC09 | R2 | Above maximum port | 65536 | INVALID |
| TC10 | R3 | HTTP protocol | http | VALID |
| TC11 | R3 | HTTPS protocol | https | VALID |
| TC12 | R3 | Unsupported protocol | ftp | INVALID |
| TC13 | R4 | Minimum valid timeout | 1 | VALID |
| TC14 | R4 | Below minimum timeout | 0 | INVALID |
| TC15 | R4 | Normal valid timeout | 30 | VALID |
| TC16 | R4 | Maximum valid timeout | 300 | VALID |
| TC17 | R4 | Above maximum timeout | 301 | INVALID |
| TC18 | R5 | Missing server field | server omitted | INVALID |
| TC19 | R5 | Missing port field | port omitted | INVALID |
| TC20 | R5 | Missing protocol field | protocol omitted | INVALID |
| TC21 | R5 | Missing timeout field | timeout omitted | INVALID |
| TC22 | R1-R5 | Completely valid configuration | All valid fields | VALID |
| TC23 | R1-R5 | Multiple invalid fields | Multiple invalid values | INVALID |
| TC24 | R1-R5 | Empty configuration | Empty file | INVALID |