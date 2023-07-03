from flask import Flask, Response, request, jsonify
import os
import openai
from flask_cors import CORS
from urllib.parse import unquote
import json
import prompt

openai_api_key = os.getenv('OPENAI_API_KEY')
openai.api_key = openai_api_key
app = Flask(__name__)
CORS(app)  # 添加这一行以允许跨域请求

@app.route("/api/backend", methods=["GET"])
def backend():
    try:
        content = request.args.get("messages", "")
        content = unquote(content)  # 解码URL参数
        content = json.loads(content)
        # content = content + "。只输出json"
        print(content)

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt.system_message},
                {"role": "user", "content": content}
            ],
            max_tokens=1000,
            n=1,
            temperature=0.1,
        )
        message = response['choices'][0]['message']['content']
        return jsonify(message=message)
    except Exception as err:
        return jsonify(error=str(err)), 404

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
    print(prompt.system_message)
    app.run(debug = True)
