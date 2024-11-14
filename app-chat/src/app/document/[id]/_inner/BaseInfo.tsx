"use client";

import FilePreview from "@/app/document/[id]/_inner/FilePreview";
import PageTitle from "@/components/PageTitle";
import {
  useDocument,
  useDocumentOutputFile,
  useDocumentRawFile,
} from "@/hooks/useDocuments";
import ragService from "@/services/RagServiceImpl";
import { DocumentStatusEnum } from "@/type/documents";
import { Button, Progress } from "@nextui-org/react";

interface BaseInfoProps {
  id: string;
}

const BaseInfo = ({ id }: BaseInfoProps) => {
  const { document } = useDocument(id);
  const haveFiles =
    document?.status === "digitized" || document.status === "embedded";
  const { rawFiles } = useDocumentRawFile(id, haveFiles);
  const { outputFiles } = useDocumentOutputFile(id, haveFiles);

  return (
    <div>
      <PageTitle title={document?.documentName} />
      <div>설명: {document?.description}</div>
      <div>버전: {document?.version}</div>
      <div>상태: {DocumentStatusEnum[document?.status ?? "default"]}</div>
      <div>페이지수: {document?.pageNum}</div>
      <p className="text-sm text-default-500 mt-1">{document?.createdAt}</p>
      <br />
      <div></div>
      {haveFiles && (
        <FilePreview
          outputFilePaths={outputFiles}
          rawFilePaths={rawFiles?.[0]}
        />
      )}
      {document.status === "error" && "error!"}
      {document.status === "pending" && (
        <div className="mt-4">
          <Progress
            aria-label="ocr-progress"
            size="md"
            value={(document.processedPageCount / document.pageNum) * 100}
            label={`OCR 진행중: ${document.processedPageCount}/${document.pageNum}`}
            color="success"
            showValueLabel={true}
            className="max-w-md"
          />
        </div>
      )}
      <br />
      <br />
      {document.status === "digitized" && (
        <Button
          className="rounded-none bg-black text-white w-[133px]"
          color="default"
          onPress={() => {
            ragService.initRag(
              document.idxName,
              document.idxName,
              document.version
            );
          }}
        >
          벡터화 저장
        </Button>
      )}
    </div>
  );
};

export default BaseInfo;
