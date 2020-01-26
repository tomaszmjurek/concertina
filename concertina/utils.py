def is_set(value):
    return not (value is None or value == 'None' or value == '')


class Options:
    BLANK = [(None, 'Fill this')]
    EMPTY = [(None, 'Leave empty to add')]

    fields_not_set = 'Some required fields were not set!'