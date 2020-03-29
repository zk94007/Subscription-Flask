"""Usage resource for handling any usage requests"""
from flask import jsonify
from webargs import fields
from webargs.flaskparser import use_kwargs
from flask import request
from flask_restful import Resource
from datetime import datetime

from src.models.usages import DataUsage
from src.models.base import db
from src.models.utils import get_object_or_404
from src.models.subscriptions import Subscription
from src.schemas.usages import UsageSchema


class UsageAPI(Resource):
    """Resource/routes for Usage endpoints"""

    def get(self, uid):
        """External facing Usage endpoint GET

        Gets an existing Usage object by id

        Args:
            sid (int): id of Subscription object

        Returns:
            json: serialized Usage object

        """
        usage = get_object_or_404(DataUsage, uid)
        result = UsageSchema().dump(usage)
        return jsonify(result.data)


class UsagesAPI(Resource):
    """Resource/routes for Usages endpoints"""
    def post(self):
        body = request.form
        usage = DataUsage(mb_used = body['mb_used'], subscription_id = body['subscription_id'],
                        from_date = datetime.strptime(body['from_date'],"%m/%d/%y"), 
                        to_date = datetime.strptime(body['to_date'],'%m/%d/%y'))

        db.session.add(usage)
        db.session.commit()
        result = UsageSchema().dump(usage)
        return jsonify(result.data)

