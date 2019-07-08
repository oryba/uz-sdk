from functools import reduce


def compose(obj, filters):
    # compose all the filter functions
    return reduce(
        lambda o, f: f(o),
        filters,
        obj
    ) if filters else obj
