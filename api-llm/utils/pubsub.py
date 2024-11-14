from dotenv import load_dotenv
import os
import redis

load_dotenv()

channels = {
    'document': 'DOCUMENT',
    'user-ocr': 'USER_OCR',
    'user-langchain': 'USER_LANGCHAIN',
    'langchain-embed': 'LANGCHAIN_EMBED'
}


class RedisPubSub:
    def __init__(self):
        url = os.environ.get("REDIS_URL")
        self.host = url.split(":")[0]
        self.port = url.split(":")[1]
        self.redis_client = redis.Redis(host=self.host, port=self.port, db=0)
        self.pubsub = self.redis_client.pubsub()
        self.subscribed_channels = set()  # 구독 채널을 저장하여 재연결 시 사용
        print("Redis에 성공적으로 연결되었습니다.")

    def connect(self):
        """Redis 서버에 연결을 시도하고 실패 시 재시도"""
        self.redis_client = redis.Redis(host=self.host, port=self.port, db=0)
        self.pubsub = self.redis_client.pubsub()
        print("Redis에 성공적으로 연결되었습니다.")

    def publish(self, channel, message):
        self.redis_client.publish(channel, message)
