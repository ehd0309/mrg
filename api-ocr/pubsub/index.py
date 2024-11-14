from dotenv import load_dotenv
import os
import threading
import json
from core import pdf_to_md_v2
import time
import redis

load_dotenv()

channels = {
    'document': 'DOCUMENT',
    'user-ocr': 'USER_OCR'
}


class RedisPubSub:
    def __init__(self):
        url = os.environ.get("REDIS_URL")
        self.host = url.split(":")[0]
        self.port = url.split(":")[1]
        self.redis_client = redis.Redis(host=self.host, port=self.port, db=0)
        self.pubsub = self.redis_client.pubsub()
        self.subscribed_channels = set()  # 구독 채널을 저장하여 재연결 시 사용

    def connect(self):
        """Redis 서버에 연결을 시도하고 실패 시 재시도"""
        while True:
            try:
                # Redis 클라이언트를 다시 생성하여 연결
                self.redis_client = redis.Redis(host=self.host, port=self.port, db=0)
                self.pubsub = self.redis_client.pubsub()
                self.resubscribe_channels()  # 재연결 시 구독 채널 복원
                print("Redis에 성공적으로 연결되었습니다.")
                break
            except redis.ConnectionError as e:
                print(f"Redis 연결 실패: {e}. 20초 후 재시도합니다...")
                time.sleep(20)

    def subscribe_document(self):
        print("subscribe documents channel")
        self.subscribed_channels.add(channels.get('document'))
        self.pubsub.subscribe(channels.get('document'))
        thread = threading.Thread(target=self.listen_to_channel)
        thread.daemon = True
        thread.start()

    def resubscribe_channels(self):
        """저장된 채널을 재구독"""
        for channel in self.subscribed_channels:
            self.pubsub.subscribe(channel)
            print(f"{channel} 채널에 대해 구독이 재설정되었습니다.")

    def listen_to_channel(self):
        """채널에서 메시지 수신 및 처리"""
        while True:
            id = ''
            try:
                for message in self.pubsub.listen():
                    if message['type'] == 'message':
                        json_message = json.loads(message['data'])
                        id = json_message.get('id')
                        index = json_message.get('idxName')
                        version = json_message.get('version')
                        results = []
                        if version == 'v2':
                            results = pdf_to_md_v2(index,
                                                   lambda msg: self.publish(channels.get('user-ocr'), msg), id)
                        if len(results) > 0:
                            self.publish(channels.get('user-ocr'), json.dumps({
                                'id': id,
                                'ocrPath': ",".join(results),
                                'status': 'digitized',
                                'pageNum': len(results),
                                'processedPageCount': len(results)
                            }))
            except Exception as e:
                if isinstance(e, redis.ConnectionError):
                    print("Redis 연결이 끊어졌습니다. 재연결을 시도합니다...")
                    self.connect()
                else:
                    self.publish(channels.get('user-ocr'), json.dumps({
                        'id': id,
                        'status': 'error'
                    }))

    def publish(self, channel, message):
        self.redis_client.publish(channel, message)
