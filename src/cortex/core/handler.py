from typing import Any


def stream_data(data: dict[str, Any], key: str) -> dict[str, Any]:
    """Stream the data.

    Args:
        result (dict[str, Any]): The result dictionary.

    Returns:
        dict[str, Any]: The streamed data.

    """
    _result = {
        'com': {
            'action': data['com'][0],
            'power': data['com'][1],
            'time': data['time'],
        },
        'fac': {
            'eyeAct': data['fac'][0],  # eye action
            'uAct': data['fac'][1],  # upper action
            'uPow': data['fac'][2],  # upper action power
            'lAct': data['fac'][3],  # lower action
            'lPow': data['fac'][4],  # lower action power
            'time': data['time'],
        },
        'eeg': {
            # FIXME(victor-iyi): Possible bug.
            'eeg': data['eeg'].pop(),  # remove markers
            'time': data['time'],
        },
        'mot': {
            'mot': data['mot'],
            'time': data['time'],
        },
        'dev': {
            'signal': data['dev'][1],
            'dev': data['dev'][2],
            'batteryPercent': data['dev'][3],
            'time': data['time'],
        },
        'met': {
            'met': data['met'],
            'time': data['time'],
        },
        'pow': {
            'pow': data['pow'],
            'time': data['time'],
        },
        'sys': data['sys'],
    }

    if key not in _result:
        raise KeyError(f'Unknown key: {key}')

    return _result[key]
