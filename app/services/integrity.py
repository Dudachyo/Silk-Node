from sqlalchemy.exc import IntegrityError


def is_unique_conflict(error: IntegrityError, constraint_name: str) -> bool:
    current = error.orig
    visited = set()
    while current is not None and id(current) not in visited:
        visited.add(id(current))
        sqlstate = getattr(current, "sqlstate", None) or getattr(current, "pgcode", None)
        name = getattr(current, "constraint_name", None)
        if sqlstate == "23505" and (name == constraint_name or constraint_name in str(current)):
            return True
        current = current.__cause__
    return False
