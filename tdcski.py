#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Copyright 2013 Bob <TDC-bob@daribouca.net>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#
__version__ = (0, 0, 1)
__author__ = 'bob'

import tdcski
import os
import sys
from tdcski import ui_server
from tdcski import alerts
from tdcski._logging import mkLogger, DEBUG

logger = mkLogger(__name__)

def main():
    # print(tdcski.config.path_to.DCS)
    # print(tdcski.config.path_to.saved_games)
    alerts.add_alert("test title", title="may Da Ribouca be with ya !", type="error")
    alerts.add_alert("test persistent", persistent=True)
    alerts.add_alert("test persistent error", persistent=True, type='error')
    alerts.add_alert("test persistent success", persistent=True, type='success')
    alerts.add_alert("test persistent info", persistent=True, type='info')
    alerts.add_alert("test persistent warning", persistent=True, type='warning')
    ui_server.main()

if __name__ == "__main__":
    main()