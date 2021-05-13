generic_permissions = {'view', 'add', 'change', 'delete'}


def get_permission_names(models):
    permission_names = set()
    model_names = [model.__name__.lower() for model in models]

    for model_name in model_names:
        for generic_permission in generic_permissions:
            permission_names.add('%s_%s' % (generic_permission, model_name))

    return permission_names
