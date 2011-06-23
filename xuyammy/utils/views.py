from django.db.models.query import QuerySet
import jsonpickle

def dict_2_json(dictionary):
    for (key, value) in dictionary.items():

        # kinda lame. better way?
        if isinstance(value, QuerySet):
            dictionary[key] = []
            for obj in value:
                dictionary[key].append(obj)

    return jsonpickle.encode(value=dictionary, unpicklable=False)
