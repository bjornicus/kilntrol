#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import os


class FileLogger(object):
    def __init__(self, filename, log_summary_interval=5*60):
        self.logfile = filename + ".log"
        self.summary_logfile = filename + "_summary.log"

        self.log_summary_interval = log_summary_interval
        self.last_log_time = -1 * log_summary_interval

        self.log_headers(self.logfile)
        self.log_headers(self.summary_logfile)

    def log_headers(self, logfile):
        if not os.path.exists(logfile):
            with open(logfile, 'w') as log:
                log.write("Time, Temperature °F, Target Temp\n")

    def log(self, t_sec, temp, target):
        str_time = time.strftime("%H:%M:%S", time.gmtime(t_sec))
        log_entry = str_time + \
            ", " + str(round(temp, 2)) + \
            ", " + str(round(target, 2)) + \
            "\n"
        with open(self.logfile, 'a') as log:
            log.write(log_entry)
        if (t_sec - self.last_log_time) > self.log_summary_interval:
            with open(self.summary_logfile, 'a') as log:
                log.write(log_entry)
            self.last_log_time = t_sec
