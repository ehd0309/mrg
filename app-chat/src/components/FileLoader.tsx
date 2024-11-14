"use client";

import { pdfjs, Document, Page } from "react-pdf";
import { useState } from "react";
import {
  CarouselProvider,
  Slider,
  Slide,
  ButtonBack,
  ButtonNext,
} from "pure-react-carousel";

import "pure-react-carousel/dist/react-carousel.es.css";
import "react-pdf/dist/Page/AnnotationLayer.css";
import "react-pdf/dist/Page/TextLayer.css";
import "core-js/full/promise/with-resolvers.js";
import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";

pdfjs.GlobalWorkerOptions.workerSrc = `//unpkg.com/pdfjs-dist@${pdfjs.version}/build/pdf.worker.min.mjs`;

const FileLoader = ({ pdfUrl, mds }: { pdfUrl: string; mds: string[] }) => {
  const [numPages, setNumPages] = useState<number>();

  function onDocumentLoadSuccess({ numPages }: { numPages: number }): void {
    setNumPages(numPages);
  }

  return (
    <CarouselProvider
      className="w-full max-h-[80dvh]"
      naturalSlideWidth={100}
      naturalSlideHeight={70}
      totalSlides={mds.length}
    >
      <Document file={pdfUrl} onLoadSuccess={onDocumentLoadSuccess}>
        <Slider className="h-[80dvh] w-full">
          {Array.from(new Array(numPages), (el, index) => (
            <Slide
              className="h-[100%] w-full overflow-y-scroll"
              key={`slide_${index + 1}`}
              index={index}
            >
              <div className="grid grid-cols-2 w-full h-full">
                <Page className="origin-left" pageNumber={index + 1} />
                <Markdown
                  className="markdown-wrapper scale-75 origin-top-left"
                  remarkPlugins={[remarkGfm]}
                >
                  {mds[index]}
                </Markdown>
              </div>
            </Slide>
          ))}
        </Slider>
      </Document>
      <div className="w-full flex justify-center gap-4 translate-y-10">
        <ButtonBack className="text-black text-md rounded-full bg-default-100 p-2">
          {"<"}
        </ButtonBack>
        <ButtonNext className="text-black text-md rounded-full bg-default-100 p-2">
          {">"}
        </ButtonNext>
      </div>
    </CarouselProvider>
  );
};

export default FileLoader;
