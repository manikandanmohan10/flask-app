from src.database.quote_model import Quote
from flask.views import MethodView
from flask import request, jsonify
from http import HTTPStatus as status
from src.database import db

class AddQuoteAPI(MethodView):
    def post(self):
        try:
            data = request.json
            quote = data.get('quote', '')
            mov_or_ser = data.get('mov/series_name', '')
            quote = Quote(quote=quote, movie_or_series=mov_or_ser)
            db.session.add(quote)
            db.session.commit()
            return jsonify('Created Successfully'), status.OK
        except Exception as e:
            return jsonify(str(e)), status.BAD_REQUEST
