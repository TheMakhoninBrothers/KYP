class EntityError(Exception):
    """Base error for entity"""


class EntityAlreadyExist(EntityError):
    """Raise if entity already existed in storage.
    For example than you try to add new entity.
    """


class EntityNotExist(EntityError):
    """Raise if entity doesn't exist in storage.
    For example than you try to search entity.
    """
