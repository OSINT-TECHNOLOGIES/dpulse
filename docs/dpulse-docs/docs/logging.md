# Logging System

DPULSE includes a comprehensive logging system that records all events and errors during program execution. Logs are essential for debugging, troubleshooting issues and reporting bugs.


---

## General Information

| Property | Value |
|---|---|
| Filename | `journal.log` |
| Location | DPULSE root directory |
| Format | Plain text |
| Created | Automatically on first launch |
| Rotation | ✅ Automatic log rotation |
| Append only | ✅ Log is never overwritten, only extended |

> 💡 Log file does not contain any sensitive information, passwords or API keys. You can safely attach it to bug reports and GitHub issues.


---

## Log Levels

DPULSE uses standard Python logging levels. You can change active log level in configuration file.

| Level | Icon | Severity | Description | When to use |
|---|---|---|---|---|
| `DEBUG` | 🔍 | 10 | Most detailed output. Records every action, request, response and internal program state. | Only when reporting a bug or troubleshooting problems. |
| `INFO` | ℹ️ | 20 | Confirmation that things are working as expected. Records all major stages of scan. | ✅ Default recommended value for normal use. |
| `WARNING` | ⚠️ | 30 | Indication of something unexpected happened, but program can continue working. | For normal operation. |
| `ERROR` | ❌ | 40 | Serious problem occurred, some function could not be completed. | Always enabled. |
| `CRITICAL` | 💥 | 50 | Fatal error, program may be unable to continue running. | Always enabled. |

> You can change log level in configuration file: `[LOGGING] log_level = info`
>
> See [Configuration File](configuration.md) for instructions.


---

## Log Format

Every log entry follows standard format:

```
YYYY-MM-DD HH:MM:SS,mmm LEVEL Process: Message
```

| Part | Description |
|---|---|
| `YYYY-MM-DD` | Date of event |
| `HH:MM:SS,mmm` | Time with millisecond precision |
| `LEVEL` | Log level of this entry |
| `Process` | Module or function that generated the entry |
| `Message` | Event description or error text |


---

## Log Structure

Log file is automatically separated between scans with clear markers:

```
==================== SCAN STARTS HERE ====================
[ all log entries for this scan ]
==================== SCAN ENDS HERE ======================
```

This makes it very easy to find logs for specific scan even if you ran hundreds of scans before.


---

## Example Log Content


![Normal log content](https://github.com/user-attachments/assets/50acae24-f024-4793-8b45-9d7e284329a6)


![Log with errors](https://github.com/user-attachments/assets/b27f8a93-115d-49ad-bf1b-c7f72613de9d)


---

## Recommendations

| Scenario | Recommended log level |
|---|---|
| Normal daily use | `info` |
| Dorking not working | `warning` |
| Unexpected behaviour | `debug` |
| Reporting a bug on GitHub | `debug` |
| Production use | `error` |


---

## Important Notes

1. ❌ Never set log level to `critical` for normal use — you will miss important warnings
2. ❌ Do not leave log level on `debug` permanently. It will generate very large log files and slightly reduce performance
3. ✅ If you are reporting an issue, always reproduce it with `log_level = debug` and attach full log file to the issue

---
