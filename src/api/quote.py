from src.database.quote_model import Quote
from flask.views import MethodView
from flask import request, jsonify
from http import HTTPStatus as status


class AddQuoteAPI(MethodView):
    def post(self):
        try:
            data = request.json
            quote = data.get('quote', '')
            mov_or_ser = data.get('mov_or_ser', '')
            return jsonify('quote'), status.OK
        except Exception as e:
            return jsonify(str(e)), status.BAD_REQUEST
