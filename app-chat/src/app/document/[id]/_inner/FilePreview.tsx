import {
  Modal,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalFooter,
  Button,
  useDisclosure,
  Spinner,
} from "@nextui-org/react";
import dynamic from "next/dynamic";
import Image from "next/image";

const PdfViewerComponent = dynamic(() => import("@/components/FileLoader"), {
  ssr: false,
});
interface FilePreviewProps {
  rawFilePaths?: string;
  outputFilePaths?: string[];
}

const FilePreview = ({ outputFilePaths, rawFilePaths }: FilePreviewProps) => {
  const { isOpen, onOpen, onOpenChange } = useDisclosure();
  const isLoading = !outputFilePaths || !rawFilePaths;

  return (
    <>
      <Button
        startContent={
          <Image src="/images/pdf.png" width={14} height={14} alt="pdf-image" />
        }
        onPress={onOpen}
        color="default"
        className="bg-black text-white"
        radius="none"
      >
        File Preview
      </Button>
      <Modal
        isOpen={isOpen}
        onOpenChange={onOpenChange}
        size="full"
        style={{ width: "85%" }}
      >
        <ModalContent>
          {(onClose) => (
            <>
              <ModalHeader className="flex flex-col gap-1">
                File Preview
              </ModalHeader>
              <ModalBody>
                {isLoading ? (
                  <Spinner
                    className="w-full h-full"
                    size="lg"
                    color="primary"
                    labelColor="primary"
                    label="문서를 불러오는 중..."
                  />
                ) : (
                  <PdfViewerComponent
                    pdfUrl={rawFilePaths}
                    mds={outputFilePaths}
                  />
                )}
              </ModalBody>
              <ModalFooter>
                <Button className="bg-black text-white" onPress={onClose}>
                  닫기
                </Button>
              </ModalFooter>
            </>
          )}
        </ModalContent>
      </Modal>
    </>
  );
};

export default FilePreview;
