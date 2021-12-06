import decimal
import difflib
from rpw import revit, DB
import System.Enum

from pyrevit import script

"""
Contains helper functions for Antler. It could be converters, formatters,
simple general functions etc...
"""

logger = script.get_logger()


def best_fuzzy_match(str_list, search_str, min=0.33):
    ratios = [(c, difflib.SequenceMatcher(None, search_str, c).ratio())
              for c in str_list]

    ratios_sorted = sorted(ratios, key=lambda x: x[1])

    best_match = ratios_sorted[-1]

    if best_match[1] > min:
        return best_match[0]
    else:
        return None


def drange(x, y, jump):
    """source: https://stackoverflow.com/questions/7267226/range-for-floats
    """
    assert jump > 0, "Jump variable must be > 0."
    while x < y:
        yield float(x)
        x += decimal.Decimal(jump)


def builtin_category_from_category(category):
    """
    Returns corresponding Builtin Category from Category.
    """
    for builtin_category in System.Enum.GetValues(DB.BuiltInCategory):
        if DB.ElementId(builtin_category).IntegerValue == category.Id.IntegerValue:
            return builtin_category
    return None


def string_from_template(element, template_string):
    import re
    """
    Use "... {Parameter Name} ... {Other Parameter Name} ..." to create strings from Elements.

    Usage:
    string_from_template(element, "{Comments} - {Mark}")

    Returns "Some comment - 123"
    """
    pattern = '\{.*?\}'
    pattern_compiled = re.compile(pattern)

    matches = re.finditer(pattern_compiled, template_string)
    logger.debug(matches)

    new_string = template_string

    for match in matches:
        logger.debug(match)
        # parameter_name = match.string[1:-1] # Python 3

        match_substring = match.string[match.start():match.end()]
        parameter_name = match_substring[1:-1]

        logger.debug(parameter_name)

        parameter = element.LookupParameter(parameter_name)

        if not parameter:
            raise ValueError, "Parameter '{}' not found".format(parameter_name)

        value = parameter.AsString() or parameter.AsValueString() or ""

        if not value:
            logger.warning(
                "Parameter '{}' has empty value".format(parameter_name))

        logger.debug("{parameter}: {value}".format(
            parameter=parameter_name, value=value))

        new_string = new_string.replace(match_substring, value)

    return new_string


def random_numbers(seed, count=1):
	"""
	Returns a list of random numbers from given seed. The seed can be anything: numbers, strings, class instances and so on.
	"""
	from System import Random

	rand = Random(int(hash(seed)))
	numbers = [rand.NextDouble() for _ in range(count)]

	return numbers


def print_dict_list_as_table(dict_list, title="", formats=[]):
    output = script.get_output()

    keys = set().union(*(d.keys() for d in dict_list))

    if not formats:
        formats = ['' for _ in keys]

    output.print_table(
        table_data=[[a.get(k) for k in keys] for a in dict_list],
        title=title,
        columns=keys,
        formats=formats
    )


def print_dict_as_table(dictionary, title="", columns=(), formats=[]):
    output = script.get_output()

    data = []

    for k, v in dictionary.items():
        # print("{}: {}".format(k, v))

        k = k.replace('\r\n', '')
        v = str(v).replace('\r\n', '')

        data.append((k, v))

    output.print_table(
        table_data=data,
        title=title,
        columns=columns or ('Key', 'Value'),
        formats=formats or ('', '')
    )


def print_dict_list(dict_list, title=""):
    """Prints a list of dictionaries as a table with keys as column names.
    """
    columns = []

    for row in dict_list:
        columns.extend(row.keys())

    columns = sorted(list(set(columns)))

    data = []

    for item in dict_list:
        data_row = []

        for key in columns:
            data_row.append(item.get(key, '-'))

        data.append(data_row)

    output = script.get_output()

    output.print_table(
        table_data=data,
        title=title,
        columns=columns
    )
