"""
Filter a json dict to remove given keys
"""


def fltr(node, vals):
    if isinstance(node, dict):
        retVal = {}
        for key in node:
            if not key in vals:
                if isinstance(node[key], list) or isinstance(node[key], dict):
                    child = fltr(node[key], vals)
                    if child:
                        retVal[key] = child
                else:
                    retVal[key] = str(node[key])
        if retVal:
            return retVal
        else:
            return None
    elif isinstance(node, list):
        retVal = []
        for entry in node:
            child = fltr(entry, vals)
            if child:
                retVal.append(child)
        if retVal:
            return retVal
        else:
            return None
