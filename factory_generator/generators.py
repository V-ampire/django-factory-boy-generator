import factory


def generate_to_dict(factory_class, fields=None):
    """
    Генерирует словарь с атрибутами на основе класса фабрики.
    :param factory_class: Класс фабрики
    :param fields: Список полей фабрики, которые нужно включить в словарь
    """
    factory_dict = factory.build(dict, FACTORY_CLASS=factory_class)
    for k in factory_dict.keys():
        try:
            if DjangoModelFactory in factory_dict[k].__bases__: # Вложенная фабрика
                factory_dict[k] = factory_as_dict(factory_dict[k])
        except AttributeError:
            # У объекта нет аттрибута '__bases__'
            pass

    if fields:
        result = {}
        for f in fields:
            result[f] = factory_dict[f]
        return result
    return factory_dict
