"""
Filter a json dict to remove given keys
"""


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
            result[key] = str(node[key])
