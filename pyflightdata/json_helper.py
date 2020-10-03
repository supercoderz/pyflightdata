# MIT License
#
# Copyright (c) 2020 Hari Allamraju
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
Filter a json dict to remove given keys
"""

import datetime

def fltr(node, vals):
    if isinstance(node, dict):
        result = {}
        for key in node:
            _process_node(key, vals, node, result)
        if result:
            return result
        else:
            return None
    elif isinstance(node, list):
        result = []
        for entry in node:
            child = fltr(entry, vals)
            if child:
                result.append(child)
        if result:
            return result
        else:
            return None


def _process_node(key, vals, node, result):
    if not key in vals:
        if isinstance(node[key], list) or isinstance(node[key], dict):
            child = fltr(node[key], vals)
            if child:
                result[key] = child
        else:
            if isinstance((node[key]), int) or isinstance((node[key]), float):
                if key in ['timestamp', 'arrival', 'departure', 'updated', 'eta', 'utc', 'local']:
                    result[key+'_millis'] = node[key] * 1000
                    result[key+'_date'] = datetime.date.fromtimestamp(node[key]).strftime('%Y%m%d')
                    result[key+'_time'] = datetime.datetime.fromtimestamp(node[key]).strftime('%H%M')
                result[key] = node[key]
            else:
                result[key] = str(node[key])
