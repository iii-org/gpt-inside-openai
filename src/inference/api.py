import os
import logging
import traceback
import datetime as dt

from utils         import complete
from flask.views   import MethodView
from flask import jsonify, request
from environment   import app
from openai.embeddings_utils import get_embedding, cosine_similarity

def search_reference(query, n=1):
    reference = app.config['REF_DATA']
    embedding = get_embedding(query, engine=os.getenv('OPENAI_ENCODER'))
    similarities = reference.embeddings.apply(lambda x: cosine_similarity(x, embedding))
    hits = sorted(enumerate(similarities), key=lambda x: x[1], reverse=True)[0]
    return reference['REF'].iloc[hits[0]], hits[1]

def error_message(message, status_code):
    error = jsonify({'status': 'error', 'message': message})
    error.status_code = status_code
    return error

class TextGenerationAPI(MethodView):

    def post(self):
        req_start_time = dt.datetime.now()
        if not request.is_json:
            return error_message('[Error Message] POST body must be a JSON format', 400)

        try:
            logger = logging.getLogger('chat_logger')
            req_data = request.get_json()
            user_input = req_data.get('user_input')
            ref_threshold = req_data.get('ref_threshold', 0)
            semantic_search = req_data.get('semantic_search', True)
            reference = req_data.get('reference')
            do_sample=req_data.get('do_sample', True)
            temperature = float(req_data.get('temperature', 0.9))
            top_p = float(req_data.get('top_p', 0.9))
            top_k = int(req_data.get('top_k', 10))
            rep = float(req_data.get('repetition_penalty', 0.6))
            gen_tokens = int(req_data.get('gen_tokens', 512))

            formatter = app.config['FORMATTER']

            if not user_input:
                raise Exception('"user_input" can not be empty.')

            result = None

            if reference:
                prompt = formatter(f"根據以下參考資料並以台灣繁體中文回答，{user_input}\n參考資料:\n{reference}\n\n").gen_text()
                ref_data, ref_score = reference, 1.0
            elif semantic_search and app.config['REF_DATA'] is not None:
                ref_data, ref_score = search_reference(user_input, ref_threshold) if not reference else (reference, 1.0)
                prompt = formatter(f"根據以下參考資料並以台灣繁體中文回答，{user_input}\n參考資料:\n{ref_data}\n\n").gen_text()
                if not ref_data:
                    result = '不好意思，我無法從參考資料中找到您需要的答案。'
            else:
                prompt = formatter(f"{user_input}\n").gen_text()
                ref_data, ref_score = None, 0.0

            if not result:
                result = complete(
                    app.config['GPT_MODEL'],
                    prompt,
                    temperature=temperature,
                    top_p=top_p,
                    max_tokens=gen_tokens,
                    frequency_penalty=rep,
                    presence_penalty=0.2
                    )

            req_end_time = dt.datetime.now()
            resp = {
                '_status': 'success',
                '_time':(req_end_time - req_start_time).total_seconds(),
                'result': {
                    'Q': user_input,
                    'ref': ref_data,
                    'A': result if isinstance(result, list) else [result]
                    }}
            logger.info(f'"{resp["_time"]}", "{os.getenv("OPENAI_ENGINE")}", "{str(prompt)}", "{str(resp["result"]["A"][0])}", "{ref_score}", "", "{temperature}", "{top_p}", "", ""')
            return jsonify(resp)
        except Exception as e:
            traceback.print_exc()
            return error_message('[Error Message] %s' % str(e), 500)

text_api = TextGenerationAPI.as_view('text-gen-api')
