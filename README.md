# Log_Monitor
Log File Monitor

Linux provides a centralized repository of log files that can be located under the  /var/log directory.

This utility helps you monitor the  most important log files and gain insight on server performance, security, error messages and underlying issues.
These are some of the log files  monitored:

* auth.log
* boot.log
* faillog
* kernlog
* maillog
* syslog
* lastlog
* rebootlog

In addition, output of some system commands are anlaysed to monitor system performance and other aspects. 

#### Usage

* To run the code, first install dependencies using 'pip install -r requirement.txt'
* From the parent folder of the cloned repository, run 'bokeh serve --show Log_Monitor/'
* After the bokeh server is created, you will be promopted to enter your system password in the terminal.
* The tool will be opened as a page in your default browser.

#### Features

* The tool gives you a condensed view of the most important log files in an interactive browser page.
* It also stores and converts the log files into a human readable csv format, for easier debugging and identification of problems.
* The browser page consists of different tabs for each  log file.
* Within each tab, there are options that can be toggled to view the different messages such as 'error messages'  and 'system messages' of each logfile.
* The logfiles have been collected and parsed using system shell commands that are called through a python script.

