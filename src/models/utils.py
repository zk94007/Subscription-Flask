"""Utilities for models to inherit or use"""
from sqlalchemy.exc import SQLAlchemyError
from flask import abort
from http import HTTPStatus


def get_object_or_404(model, mid):
    """Get an object by id or return a 404 not found response

    Args:
        model (object): object's model class
        mid (int): object's id

    Returns:
        object: returned from query

    Raises:
        404: if one object is returned from query

    """
    try:
        return model.query.get(mid)
    except SQLAlchemyError:
        abort(404)
