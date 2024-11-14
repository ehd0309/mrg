export enum RedisChannel {
  // To Publish
  DOCUMENT = "DOCUMENT",
  LANGCHAIN_EMBED = "LANGCHAIN_EMBED",

  // To Subscribe
  USER_OCR = "USER_OCR",
  USER_LANGCHAIN = "USER_LANGCHAIN",
}
