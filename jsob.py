import click, json, sys, math

JSON_KEYWORDS = ["true", "false", "null"]

@click.group()
def cli():
    """This script will assemble a JSON structure (an object or a array) from
    strings (containing JSON values: a string, a number, an object, an array,
    a boolean, or `null`) arguments."""
    pass

@cli.command()
@click.argument('value', nargs=-1)
@click.option('--tuple/--list', 'tuple_list', default=True,
              help="Accept a list of tuples (JSON key-value pairs) or a tuple of "
                   "lists (a list of JSON keys & a list of JSON values) to zip "
                   "into an object; defaults to accepting a list of tuples.")
@click.option('--cast-keys-to-string/--parse-key-types', default=False,
              help="Strings are the only acceptable type for JSON object keys; "
                   "this option selects whether to cast all keys to strings, or "
                   "to attempt to parse the keys' types, and raise an error if "
                   "they can be iterpreted as non-strings. Defaults to parsing "
                   "key types.")
def object(value, tuple_list, cast_keys_to_string):
    """Assemble a JSON object - curly-brace delimited list of pairs, with string
    keys and JSON-acceptible values, possibly empty. If an odd number of values
    are provided, the last value will be discarded."""
    if tuple_list:
       keys = value[::2]
       values = value[1::2]
    else:
        num_pairs = math.floor(len(value) / 2.0)
        keys = value[:num_pairs]
        values = value[num_pairs:]

    # all keys must be strings
    if not cast_keys_to_string:
        for key in keys:
            type_json_value(key, str)
        values = map(json_try_cast, values)

    click.echo(json.dumps(dict(zip(keys, values))))

@cli.command()
@click.argument('element', nargs=-1)
def array(element):
    """Assemble a JSON array - a square-bracket delimited list of
    JSON-acceptible values, possibly empty."""
    click.echo(json.dumps(list(map(json_try_cast, element))))

@cli.command(name="type")
@click.argument('value', nargs=-1)
def type_value(value):
    """Display the type of the input JSON values, one per line."""
    for value_type_string in map(type_json_value, value):
        click.echo(value_type_string)

def json_try_cast(value):
    """Attempts to turn the input string (representing a JSON value) into a
    sensible Python object; else, raise a ValueError."""
    try:
        return(float(value))
    except ValueError:
        # value error does not rule out parsing into other types
        pass

    if (value not in JSON_KEYWORDS) and \
      (('{' not in value) and ('}' not in value)) and \
      (('[' not in value) and (']' not in value)):
        return value

    try:
        return json.loads(value)
    except:
        raise ValueError("Could not correctly type the value '{}'".format(value))

def type_json_value(value, target_type=None):
    """If the input value string can be correctly cast (see `json_try_cast`),
    return its type.

    If `target_type` is passed, returns `True` if the input value is an instance
    of that type and `False` if it is not."""
    cast_value = json_try_cast(value)
    if target_type is not None:
        if not isinstance(cast_value, target_type):
            raise ValueError("Could not correctly cast the value '{}' to {}"\
                                .format(cast_value, target_type))

    return type(cast_value)
