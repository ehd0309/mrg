"use client";

import { useDocumentList } from "@/hooks/useDocuments";
import useRagCreate from "@/hooks/useRagCreate";
import {
  Modal,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalFooter,
  Button,
  useDisclosure,
  Input,
  CheckboxGroup,
  Checkbox,
} from "@nextui-org/react";
import { useRouter } from "next/navigation";
import { useState } from "react";

const RagUploader = () => {
  const router = useRouter();
  const { documents } = useDocumentList();
  const { isOpen, onOpen, onOpenChange, onClose } = useDisclosure();
  const [name, setName] = useState<string>("");
  const [documentIds, setDocumentIds] = useState<string[]>([
    documents?.[0]?.id?.toString() ?? "",
  ]);

  const { createRag } = useRagCreate();

  const handleSubmit = async () => {
    if (name === "" || documentIds.length === 0) {
      alert("이름 또는 문서 목록이 비어있습니다");
    }
    await createRag({
      documents: documents.filter((d) => documentIds.includes(d.id.toString())),
      name: name,
    }).then((r) => {
      setTimeout(() => {
        router.push("/chat" + r.id);
      }, 2000);
    });
    onClose();
  };

  return (
    <>
      <Button
        onPress={onOpen}
        fullWidth
        color="default"
        className="bg-black text-white"
        radius="none"
      >
        RAG QnA 등록
      </Button>
      <Modal isOpen={isOpen} onOpenChange={onOpenChange}>
        <ModalContent>
          {(onClose) => (
            <>
              <ModalHeader className="flex flex-col gap-1">
                RAG QnA 등록
              </ModalHeader>
              <ModalBody>
                <Input
                  type="text"
                  label="QnA 이름"
                  value={name}
                  onValueChange={setName}
                />
                <CheckboxGroup
                  label="Select cities"
                  color="warning"
                  value={documentIds}
                  onValueChange={setDocumentIds}
                >
                  {documents.map((d) => (
                    <Checkbox key={d.id} value={d.id.toString()}>
                      {d.documentName}
                    </Checkbox>
                  ))}
                </CheckboxGroup>
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

export default RagUploader;
