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

import sys
import logging

from atomicapp.constants import (LOGGER_COCKPIT,
                                 LOGGER_DEFAULT)


class colorizeOutputFormatter(logging.Formatter):
    """
    A class to colorize the log msgs based on log level
    """

    def format(self, record):
        # Call the parent class to do formatting.
        msg = super(colorizeOutputFormatter, self).format(record)

        # Now post process and colorize if needed
        if record.levelno == logging.DEBUG:
            msg = self._colorize(msg, 'cyan')
        elif record.levelno == logging.WARNING:
            msg = self._colorize(msg, 'yellow')
        elif record.levelno == logging.INFO:
            msg = self._colorize(msg, 'white')
        elif record.levelno == logging.ERROR:
            msg = self._colorize(msg, 'red')
        else:
            raise Exception("Invalid logging level {}".format(record.levelno))
        return self._make_unicode(msg)

    def _colorize(self, text, color):
        """
        Colorize based upon the color codes indicated.
        """
        # Console colour codes
        colorCodes = {
            'white': '0', 'bright white': '1;37',
            'blue': '0;34', 'bright blue': '1;34',
            'green': '0;32', 'bright green': '1;32',
            'cyan': '0;36', 'bright cyan': '1;36',
            'red': '0;31', 'bright red': '1;31',
            'purple': '0;35', 'bright purple': '1;35',
            'yellow': '0;33', 'bright yellow': '1;33',
        }
        return "\033[" + colorCodes[color] + "m" + text + "\033[0m"

    def _make_unicode(self, input):
        """
        Convert all input to utf-8 for multi language support
        """
        if type(input) != unicode:
            input = input.decode('utf-8')
        return input


class Logging:

    @staticmethod
    def setup_logging(verbose=None, quiet=None, outputtype=None):
        """
        This function sets up logging based on the outputtype requested.
        The 'none' level outputs not logs at all
        The 'cockpit' level outputs just logs for the cockpit logger
        The 'stdout' level prints out normal log msgs (no cockpit) without color
        The 'default' level prints out normal log msgs (no cockpit) with color
        """

        # If no outputtype was set then let's have a sane default
        # If connected to a tty, then default to color, else, no color
        if not outputtype:
            if sys.stdout.isatty():
                outputtype = 'stdoutcolor'
            else:
                outputtype = 'stdout'

        # Determine what logging level we should use
        if verbose:
            logging_level = logging.DEBUG
        elif quiet:
            logging_level = logging.WARNING
        else:
            logging_level = logging.INFO

        # Get the loggers and clear out the handlers (allows this function
        # to be run more than once)
        logger = logging.getLogger(LOGGER_DEFAULT)
        logger.handlers = []
        cockpitlogger = logging.getLogger(LOGGER_COCKPIT)
        cockpitlogger.handlers = []

        if outputtype == 'none':
            # blank out both loggers
            logger.addHandler(logging.NullHandler())
            cockpitlogger.addHandler(logging.NullHandler())
            return

        if outputtype == 'cockpit':
            # blank out normal log messages
            logger.addHandler(logging.NullHandler())

            # configure cockpit logger
            handler = logging.StreamHandler(stream=sys.stdout)
            formatter = logging.Formatter('atomicapp.status.%(levelname)s.message=%(message)s')
            handler.setFormatter(formatter)
            cockpitlogger.addHandler(handler)
            cockpitlogger.setLevel(logging_level)
            return

        if outputtype == 'stdout':
            # blank out cockpit log messages
            cockpitlogger = logging.getLogger(LOGGER_COCKPIT)
            cockpitlogger.addHandler(logging.NullHandler())

            # configure logger for basic printing to stdout
            handler = logging.StreamHandler(stream=sys.stdout)
            formatter = logging.Formatter('%(asctime)s - [%(levelname)s] - %(filename)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging_level)
            return

        if outputtype == 'stdoutcolor':
            # blank out cockpit log messages
            cockpitlogger.addHandler(logging.NullHandler())

            # configure logger for color printing to stdout
            handler = logging.StreamHandler(stream=sys.stdout)
            formatter = colorizeOutputFormatter('%(asctime)s - [%(levelname)s] - %(filename)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging_level)
            return

        # If we made it here then there is an error
        raise Exception("Invalid logging output type: {}".format(outputtype))
