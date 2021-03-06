import re


def remove_preceding_slash(path: str):
    return path[1:] if len(path) > 1 and path[0] == "/" else path


def camel_to_pretty(raw):
    return ' '.join(re.findall(r'[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', raw))


def pretty_title(raw: str) -> str:
    if '_' in raw:
        return ' '.join(x[0].upper() + x[1:] for x in raw.split('_'))
    elif any(x.isupper() for x in raw):
        if raw[0].islower():
            new_raw = raw[0].upper() + raw[1:]
        else:
            new_raw = raw
        return camel_to_pretty(new_raw)
    else:
        return raw[0].upper() + raw[1:]
