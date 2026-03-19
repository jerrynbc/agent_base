from flask import Flask, render_template, request, jsonify
from agent import agent
from config import config

app = Flask(__name__, template_folder='../templates')

@app.route('/')
def index():
    return render_template('index.html', config=config.get_config())

@app.route('/api/config', methods=['POST'])
def update_config():
    """更新配置"""
    config_data = request.json
    agent.update_config(config_data)
    return jsonify({"status": "success", "config": config.get_config()})

@app.route('/api/chat', methods=['POST'])
def chat():
    """对话接口"""
    data = request.json
    user_input = data.get('message', '')
    response = agent.generate_response(user_input)
    return jsonify({"response": response, "history": agent.get_chat_history()})

@app.route('/api/clear-history', methods=['POST'])
def clear_history():
    """清空对话历史"""
    agent.clear_chat_history()
    return jsonify({"status": "success"})

@app.route('/health')
def health():
    """健康检查"""
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)