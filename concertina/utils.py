def is_set(value):
    return not (value is None or value == 'None' or value == '')


def filter_by_query(set, query):
    return [item for item in set if any(query in str(x).lower() for x in item.values())]


class Options:
    BLANK = [(None, 'Fill this')]
    EMPTY = [(None, 'Leave as it is to add')]

    fields_not_set = 'Some required fields were not set!'