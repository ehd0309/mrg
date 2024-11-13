import fs from "fs";
import path from "path";
import { InternalServerError } from "routing-controllers";

export const uploadFile = async (
  file: Express.Multer.File,
  name: string,
  savePath: string
) => {
  const directoryPath = path.join(savePath);
  const filePath = path.join(directoryPath, name);

  try {
    await fs.promises.mkdir(directoryPath, { recursive: true });
    await fs.promises.writeFile(filePath, file.buffer);
    return filePath;
  } catch {
    throw new InternalServerError("파일 업로드에 실패했습니다");
  }
};
