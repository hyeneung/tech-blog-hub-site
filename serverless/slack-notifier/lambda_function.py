import json
import base64
import gzip
import os
import urllib.request

# 환경 변수에서 Slack Webhook URL 가져오기
SLACK_WEBHOOK_URL = os.environ['SLACK_WEBHOOK_URL']

def send_slack_message(message):
    data = json.dumps({"text": message}).encode('utf-8')
    req = urllib.request.Request(SLACK_WEBHOOK_URL, data=data, method='POST')
    req.add_header('Content-Type', 'application/json')
    
    try:
        with urllib.request.urlopen(req) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"Error sending message to Slack: {e}")
        return None

def lambda_handler(event, context):
    # CloudWatch Logs 데이터 디코딩
    compressed_payload = base64.b64decode(event['awslogs']['data'])
    uncompressed_payload = gzip.decompress(compressed_payload)
    payload = json.loads(uncompressed_payload)

    # 로그 그룹 및 스트림 정보
    log_group = payload['logGroup']
    log_stream = payload['logStream']

    # 로그 이벤트 처리
    for log_event in payload['logEvents']:
        message = log_event['message'].lower()  # 모든 문자를 소문자로 변환
        if 'error' in message or 'warn' or '500' in message:
            slack_message = f"*Log Group:* {log_group}\n*Log Stream:* {log_stream}\n*Message:* {message}"
            response = send_slack_message(slack_message)
            if response:
                print(f"Message sent to Slack successfully: {response}")
            else:
                print("Failed to send message to Slack")

    return {
        'statusCode': 200,
        'body': json.dumps('Log processing completed')
    }