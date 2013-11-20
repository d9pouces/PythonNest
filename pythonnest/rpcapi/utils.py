from django.db.models import Q

__author__ = 'flanker'


def prepare_query(previous_query, prefix, key, value, global_and=True):
    kwargs = {}
    if (isinstance(value, list) or isinstance(value, tuple)) and len(value) > 1:
        kwargs = {prefix + key + '__in': value}
    elif isinstance(value, list) or isinstance(value, tuple):
        value = value[0]
    if not kwargs:
        if value[:1] == '*' and value[-1:] == '*':
            kwargs = {prefix + key + '__icontains': value[1:-1]}
        elif value[:1] == '*':
            kwargs = {prefix + key + '__iendswith': value[1:]}
        elif value[-1:] == '*':
            kwargs = {prefix + key + '__istartswith': value[:-1]}
        else:
            kwargs = {prefix + key + '__iexact': value}
    if previous_query is None:
        return Q(**kwargs)
    elif global_and:
        return previous_query & Q(**kwargs)
    return previous_query | Q(**kwargs)
