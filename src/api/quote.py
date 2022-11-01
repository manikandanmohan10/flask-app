import logging
from src.models.quote_model import Quote
from flask.views import MethodView
from flask import request, jsonify
from http import HTTPStatus as status
from src.models import db


class AddQuoteAPI(MethodView):
    def post(self):
        try:
            data = request.json
            payload = request.environ.get('payload')
            user_id = payload.get('sub')

            quote = data.get('quote', '')
            mov_or_ser = data.get('mov/series_name', '')
            quote = Quote(quote=quote, movie_or_series=mov_or_ser, user_id=user_id)
            db.session.add(quote)
            db.session.commit()
            logging.info('created successfully')
            return jsonify('Created Successfully'), status.OK
        except Exception as e:
            logging.warning(f'Exception -> {str(e)}')
            return jsonify(str(e)), status.BAD_REQUEST
