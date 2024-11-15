"use client";

import useDocumentCreate from "@/hooks/useDocumentCreate";
import {
  Modal,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalFooter,
  Button,
  useDisclosure,
  Input,
} from "@nextui-org/react";
import Image from "next/image";
import { useRouter } from "next/navigation";
import { useState } from "react";

const DocumentUploader = () => {
  const router = useRouter();
  const { isOpen, onOpen, onOpenChange, onClose } = useDisclosure();
  const [file, setFile] = useState<File | null>(null);
  const [fileName, setFileName] = useState<string>("");
  const [fileDescription, setFileDescription] = useState<string>("");

  const { createDocument } = useDocumentCreate();

  const handleSubmit = async () => {
    const blob = new Blob([file as BlobPart], { type: "application/pdf" });
    const res = await createDocument({
      document: blob,
      name: fileName,
      description: fileDescription,
      version: "v2",
    });
    onClose();
  };

  return (
    <>
      <Button
        startContent={
          <Image src="/images/pdf.png" width={14} height={14} alt="pdf-image" />
        }
        onPress={onOpen}
        fullWidth
        color="default"
        className="bg-black text-white"
        radius="none"
      >
        문서 등록
      </Button>
      <Modal isOpen={isOpen} onOpenChange={onOpenChange}>
        <ModalContent>
          {(onClose) => (
            <>
              <ModalHeader className="flex flex-col gap-1">
                문서 등록하기
              </ModalHeader>
              <ModalBody>
                <p>OCR부터 데이터 저장까지 자동으로 수행합니다.</p>
                <Input
                  type="text"
                  label="문서 이름"
                  value={fileName}
                  onValueChange={setFileName}
                />
                <Input
                  type="text"
                  label="문서 설명"
                  value={fileDescription}
                  onValueChange={setFileDescription}
                />
                <Input
                  type="file"
                  label="문서 파일"
                  onChange={(e: any) => {
                    setFile(e.target.files[0]);
                  }}
                  accept="application/pdf"
                />
              </ModalBody>
              <ModalFooter>
                <Button
                  className="bg-white text-dark"
                  variant="light"
                  onPress={onClose}
                >
                  Close
                </Button>
                <Button className="bg-black text-white" onPress={handleSubmit}>
                  등록하기
                </Button>
              </ModalFooter>
            </>
          )}
        </ModalContent>
      </Modal>
    </>
  );
};

export default DocumentUploader;
