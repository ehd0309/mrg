import fs from "fs";
import path from "path";
import archiver from "archiver";

import { InternalServerError } from "routing-controllers";
import { logger } from "@/logger";

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

export const archiveFiles = async (paths: string[], res: any) => {
  const files = paths.map((filePath) => ({
    name: path.basename(filePath),
    path: filePath,
  }));
  console.log(files);
  const archive = archiver("zip", {
    zlib: { level: 9 },
  });

  archive.on("error", (err) => {
    logger.error({
      message: `압축 중 오류가 발생했습니다. with ${err}`,
      url: "ARCHIVE",
      method: "GET",
    });
    throw new InternalServerError("압축 중 오류가 발생했습니다");
  });

  archive.pipe(res);

  files.forEach((file) => {
    archive.file(file.path, { name: file.name });
  });

  return await archive.finalize();
};

export const getMdFilesFromFolders = async (
  folderPaths: string[]
): Promise<string[]> => {
  const mdFiles: string[] = [];
  for (const folderPath of folderPaths) {
    try {
      const files = fs.readdirSync(folderPath);
      for (const file of files) {
        if (file.endsWith(".md")) {
          mdFiles.push(path.join(folderPath, file));
        }
      }
    } catch (error) {
      logger.error({
        message: `md 파일을 읽는 중 오류 발생. with ${error}`,
        url: "FILE_READ",
        method: "GET",
      });
      throw new InternalServerError("파일 로드 중 오류가 발생했습니다");
    }
  }
  return mdFiles;
};
