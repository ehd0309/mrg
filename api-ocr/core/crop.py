import fitz  # PyMuPDF


def crop_pdf_top_bottom(input_pdf_path, output_pdf_path, crop_px_lower=45, crop_px_upper=45):
    # PDF 파일 열기
    pdf_document = fitz.open(input_pdf_path)

    # 새로운 PDF를 저장할 빈 문서 생성
    output_pdf = fitz.open()

    # 각 페이지에 대해 상하단 50px 잘라내기
    for page_number in range(pdf_document.page_count):
        page = pdf_document.load_page(page_number)

        # 페이지 크기 가져오기
        rect = page.rect
        # 상단과 하단의 50px을 잘라낸 새로운 사각형 영역 설정
        cropped_rect = fitz.Rect(
            rect.x0,
            rect.y0 - crop_px_upper,  # 상단 50px 잘라내기
            rect.x1,
            rect.y1 - crop_px_lower  # 하단 50px 잘라내기
        )

        # 잘라낸 영역을 복사해서 새로운 페이지로 추가
        cropped_page = output_pdf.new_page(width=rect.width, height=cropped_rect.height)
        cropped_page.show_pdf_page(cropped_page.rect, pdf_document, page_number, clip=cropped_rect)

    # 새 PDF 파일로 저장
    output_pdf.save(output_pdf_path)
    output_pdf.close()
    pdf_document.close()


# 사용 예시
# input_pdf_path = "../assets/test/원광대의무기록.pdf"
# output_pdf_path = "../assets/test/원광-c.pdf"
# crop_pdf_top_bottom(input_pdf_path, output_pdf_path)
