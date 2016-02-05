"""
 Copyright 2015 Red Hat, Inc.

 This file is part of Atomic App.

 Atomic App is free software: you can redistribute it and/or modify
 it under the terms of the GNU Lesser General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 Atomic App is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU Lesser General Public License for more details.

 You should have received a copy of the GNU Lesser General Public License
 along with Atomic App. If not, see <http://www.gnu.org/licenses/>.
"""

import os
import sys
import time
import logging
import logging.handlers
from atomicapp.constants import LOG_NAME, LOG_LEVELS, LOG_CUSTOM_NAME, LOG_SYSLOG


class Display:

    '''

    In order to effectively use logging within Python, we manipulate the level
    codes by adding our own custom ones. By doing so, we are able to have different
    log legs effectively span all Python files.

    Upon initialization, Atomic App checks to see if --logging-ouput= is set during
    initalization and set's the appropriate log level based on either the default
    or custom level value.

    Default python level codes

    NOTSET    0
    DEBUG    10
    INFO     20
    WARNING  30
    ERROR    40
    CRITICAL 50

    Custom log levels in constants.py

    LOG_LEVELS = {
        "default": 90,
        "cockpit": 91,
        "stdout": 92,
        "syslog": 93,
        "none": 94
    }

    '''

    # Console colour codes
    codeCodes = {
        'black': '0;30', 'bright gray': '0;37',
        'blue': '0;34', 'white': '1;37',
        'green': '0;32', 'bright blue': '1;34',
        'cyan': '0;36', 'bright green': '1;32',
        'red': '0;31', 'bright cyan': '1;36',
        'purple': '0;35', 'bright red': '1;31',
        'yellow': '0;33', 'bright purple': '1;35',
        'dark gray': '1;30', 'bright yellow': '1;33',
        'normal': '0'
    }

    # Upon initialization we grab the log level value and verbose level (-v or not)
    def __init__(self):
        self.logger = logging.getLogger(LOG_NAME)
        self.verbose_level = self.logger.getEffectiveLevel()
        self.log_level = logging.getLogger(LOG_CUSTOM_NAME).getEffectiveLevel()

    def debug(self, msg, only=None):
        self.display(msg, 10, 'cyan', only)

    def verbose(self, msg, only=None):
        self.display(msg, 10, 'cyan', only)

    def info(self, msg, only=None):
        self.display(msg, 20, 'green', only)

    def warning(self, msg, only=None):
        self.display(msg, 30, 'yellow', only)

    def error(self, msg, only=None):
        self.display(msg, 40, 'red', only)

    # Display checks to see what log_level is being matched to and passes it along to
    # the logging provider
    def display(self, msg, code, color, only):
        if self.log_level == LOG_LEVELS['cockpit']:
            self._cockpit(msg, code, only)
        elif self.log_level == LOG_LEVELS['stdout']:
            self._stdout(msg, code)
        elif self.log_level == LOG_LEVELS['syslog']:
            self._syslog(msg, code)
        elif self.log_level == LOG_LEVELS['none']:
            return
        else:
            self._default(msg, code, color)

    # Make sure that we're outputting stdout or stderr each time
    def _sysflush(self):
        if self.verbose_level is LOG_LEVELS['error'] or self.verbose_level is LOG_LEVELS['warning']:
            sys.stderr.flush()
        else:
            sys.stdout.flush()

    # Due to cockpit logging requirements, we will ONLY output logging that is designed as
    # display.info("foo bar", "cockpit")
    def _cockpit(self, msg, code, only):
        if only is not "cockpit":
            return

        if self.verbose_level is not LOG_LEVELS['debug'] and code is LOG_LEVELS['debug']:
            return

        if code == LOG_LEVELS['debug']:
            msg = "atomicapp.status.debug.message=%s" % msg
        elif code == LOG_LEVELS['warning']:
            msg = "atomicapp.status.warning.message=%s" % msg
        elif code == LOG_LEVELS['error']:
            msg = "atomicapp.status.error.message=%s" % msg
        else:
            msg = "atomicapp.status.info.message=%s" % msg

        self._sysflush()
        print(self._make_unicode(msg))

    def _syslog(self, msg, code):
        if self.verbose_level is not LOG_LEVELS['debug'] and code is LOG_LEVELS['debug']:
            return

        # Don't output anything, but everything into the syslog (/var/log/atomicapp.log)
        handler = logging.handlers.SysLogHandler(address=LOG_SYSLOG)
        self.logger.handlers = []
        self.logger.addHandler(handler)

        if code == LOG_LEVELS['debug']:
            self.logger.info(msg)
        elif code == LOG_LEVELS['warning']:
            self.logger.warning(msg)
        elif code == LOG_LEVELS['error']:
            self.logger.error(msg)
        else:
            self.logger.info(msg)

    def _default(self, msg, code, color):
        if self.verbose_level is not LOG_LEVELS['debug'] and code is LOG_LEVELS['debug']:
            return

        if code == LOG_LEVELS['debug']:
            self.logger.info(msg)
            msg = "[DEBUG] %6d %0.2f %s" % (os.getpid(), time.time(), msg)
        elif code == LOG_LEVELS['warning']:
            self.logger.warning(msg)
            msg = "[WARNING] %s" % msg
        elif code == LOG_LEVELS['error']:
            self.logger.error(msg)
            msg = "[ERROR] %s" % msg
        else:
            self.logger.info(msg)
            msg = "[INFO] %s" % msg

        self._sysflush()
        print(self._colorize(self._make_unicode(msg), color))

    def _stdout(self, msg, code):
        if self.verbose_level is not LOG_LEVELS['debug'] and code is LOG_LEVELS['debug']:
            return

        if code == LOG_LEVELS['debug']:
            msg = "[DEBUG] %6d %0.2f %s" % (os.getpid(), time.time(), msg)
        elif code == LOG_LEVELS['warning']:
            msg = "[WARNING] %s" % msg
        elif code == LOG_LEVELS['error']:
            msg = "[ERROR] %s" % msg
        else:
            msg = "[INFO] %s" % msg

        self._sysflush()
        print(self._make_unicode(msg))

    # Colors!
    def _colorize(self, text, color):
        return "\033[" + self.codeCodes[color] + "m" + text + "\033[0m"

    # Convert all those pesky log messages to utf-8
    def _make_unicode(self, input):
        if type(input) != unicode:
            input = input.decode('utf-8')
            return input
        else:
            return input


def set_logging(args):
    if args.verbose:
        level = logging.DEBUG
    elif args.quiet:
        level = logging.WARNING
    else:
        level = logging.INFO

    # Let's check to see if any of our choices match the LOG_LEVELS constant! --logging-output
    for k in LOG_LEVELS:
        if hasattr(args, 'logging_output') is False:
            custom_level = LOG_LEVELS['default']
            break
        elif args.logging_output == k:
            custom_level = LOG_LEVELS[args.logging_output]
            break
        # This should not ever reach here if using "choices" in CLI options
        else:
            custom_level = LOG_LEVELS['default']

    logging.getLogger(LOG_NAME).setLevel(level)
    logging.getLogger(LOG_CUSTOM_NAME).setLevel(custom_level)
