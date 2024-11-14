import { logger } from "@/logger";
import { RedisChannel } from "@/types/redis";
import { createClient, RedisClientType } from "redis";
import { BadRequestError } from "routing-controllers";
import Container, { Service } from "typedi";

@Service()
export class RedisService {
  private redisClient: RedisClientType;
  private subscriber: RedisClientType;

  private subscribedChannels: Map<
    RedisChannel,
    (msg?: string) => void | Promise<void>
  > = new Map();

  constructor() {
    this.redisClient = createClient({
      url: process.env.REDIS_URL || "redis://localhost:10686",
    });
    this.subscriber = this.redisClient.duplicate();

    this.subscriber.on("ready", () => {
      this.resubscribeChannels();
      logger.info({
        message: `Redis Subscriber가 준비되었습니다. with ${JSON.stringify(
          this.subscribedChannels
        )}`,
        url: "REDIS",
        method: "GET",
      });
    });
  }

  public async initialize() {
    try {
      await this.redisClient.connect();
      await this.subscriber.connect();
      logger.info({
        message: "Redis에 성공적으로 연결되었습니다.",
        url: "REDIS",
        method: "GET",
      });
    } catch (error) {
      logger.error({
        method: "GET",
        url: "REDIS",
        message: `Redis 연결 중 오류가 발생했습니다. with ${error}`,
      });
      throw new Error("Redis 연결 실패");
    }
  }

  public async disconnect() {
    await this.redisClient.disconnect();
    await this.subscriber.disconnect();
    logger.info({
      message: "Redis 연결 종료",
      url: "REDIS",
      method: "DELETE",
    });
  }

  public getRedisClient() {
    return this.redisClient;
  }

  // 기존 채널 구독 복원 메서드
  private async resubscribeChannels() {
    for (const [channel, handler] of this.subscribedChannels.entries()) {
      await this.subscriber.subscribe(channel, (message) => {
        logger.info({
          message: `재연결 후 수신한 메시지: ${message}`,
          url: "REDIS",
          method: "GET",
        });
        handler(message);
      });
      logger.info({
        message: `채널 ${channel}에 대한 구독이 재설정되었습니다.`,
        url: "REDIS",
        method: "GET",
      });
    }
  }

  public async subscribe(
    channel: RedisChannel,
    handler: (msg?: string) => void | Promise<void>
  ) {
    try {
      // 구독 설정 및 메시지 수신 시 핸들러 호출
      await this.subscriber.subscribe(channel, (message) => {
        logger.info({
          message: `수신한 메시지: ${message}`,
          url: "REDIS",
          method: "GET",
        });
        handler(message);
      });
      // 채널과 핸들러를 Map에 저장하여 재연결 시 복원
      this.subscribedChannels.set(channel, handler);
    } catch (error) {
      logger.error({
        method: "GET",
        url: "REDIS",
        message: `Redis 구독 오류. with ${error}`,
      });
      throw new Error("Redis 구독 실패");
    }
  }

  public async unsubscribe(channel: RedisChannel) {
    await this.subscriber.unsubscribe(channel);
    this.subscribedChannels.delete(channel); // 구독 목록에서 채널 제거
  }

  public async publish(channel: RedisChannel, message: string) {
    try {
      await this.redisClient.publish(channel, message);
      logger.info({
        message: `발신한 메시지: ${message} for ${channel}`,
        url: "REDIS",
        method: "POST",
      });
    } catch (error) {
      logger.error({
        method: "POST",
        url: "REDIS",
        message: `Redis 발신 오류. with ${error}`,
      });
      throw new BadRequestError("Redis publish error");
    }
  }
}

export const redisInstance = () => Container.get(RedisService);
