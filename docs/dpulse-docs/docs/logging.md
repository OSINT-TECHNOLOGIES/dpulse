# About logging

Logging is a way to record events and messages that occur during the execution of a program, which helps in debugging and monitoring the application's behavior. Since DPULSE is written on Python, it uses in-built ***logging*** method.

## Levels of logging

There are five built-in levels of the log message which are supported in DPULSE:  

- Debug (used to give Detailed information, typically of interest only when diagnosing problems)
- Info (used to confirm that things are working as expected)
- Warning (used as an indication that something unexpected happened, or is indicative of some problem in the near future)
- Error (tells that due to a more serious problem, the software has not been able to perform some function)
- Critical (tells serious error, indicating that the program itself may be unable to continue running)

You can use these levels according to your needs by editing the configuration file. You can read more about changing configuration parameters in 'Configuration file' paragraph.

## How it looks like in practice

In DPULSE, first creation of logging file (journal.log) happens with first DPULSE start, and first strings in log file will appear with first scan. Standard string in this file contains date (YYYY-MM-DD format), time (HH:MM:SS, MS format), level of config, process name and its status (additionaly string contains full error if status was bad). Also DPULSE separates log info for each scan with STARTS HERE and ENDS HERE lines. Content of log file looks like that:

![logging](https://github.com/user-attachments/assets/50acae24-f024-4793-8b45-9d7e284329a6)

![logging2](https://github.com/user-attachments/assets/b27f8a93-115d-49ad-bf1b-c7f72613de9d)
