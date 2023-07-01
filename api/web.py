from flask import Flask, Response, request, jsonify
import os
import openai
from flask_cors import CORS
from urllib.parse import unquote
import json

openai_api_key = os.getenv('OPENAI_API_KEY')
openai.api_key = openai_api_key
app = Flask(__name__)
CORS(app)  # 添加这一行以允许跨域请求

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    print(request.args)
    key = request.args.get('key')
    return Response("<h1>Flask</h1><p>You visited: /%s</p><p>key=%s</p>" % (path,key), mimetype="text/html")

@app.route("/api/chart", methods=["GET"])
def chart():
        print(request.args)
        key = request.args.get('key')
        return Response("<h1>Flask</h1><p>You key: </p><p>key=%s</p>" % (openai_api_key), mimetype="text/html")
    


@app.route("/api/chatmesg", methods=["GET"])
def chatmesg():
    try:
        messages = request.args.get("messages", "")
        messages = unquote(messages)  # 解码URL参数
        messages = json.loads(messages)
        print(messages)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=1000,
            n=1,
            temperature=0.1,
        )
        message = response['choices'][0]['message']['content']
        return jsonify(message=message)
    except Exception as err:
        return jsonify(error=str(err)), 404
    
if __name__ == "__main__":
    app.run(debug = True)
