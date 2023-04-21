"""Token system

The capture gui application will format tokens in the filename.
The tokens can be registered using `register_token`

"""
_registered_tokens = dict()

def get_user_name() -> str :
    import getpass
    return getpass.getuser()

def format_tokens(string, options):
    """Replace the tokens with the correlated strings

    Arguments:
        string (str): filename of the playblast with tokens.
        options (dict): The parsed capture options.

    Returns:
        str: The formatted filename with all tokens resolved

    """

    if not string:
        return string

    for token, value in _registered_tokens.items():
        if token in string:
            func = value['func']
            string = string.replace(token, func(options))

    return string

def register_token(token, func, label=""):
    assert token.startswith("<") and token.endswith(">")
    assert callable(func)
    _registered_tokens[token] = {"func": func, "label": label}

def list_tokens():
    return _registered_tokens.copy()

register_token("<user>",
                lambda options :get_user_name(),
                label="Insert current user's name")
