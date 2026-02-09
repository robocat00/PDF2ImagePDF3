import fitz
from PIL import Image
import io
import os
from tkinter import (
    Tk, filedialog, messagebox,
    Label, Button, StringVar,
    OptionMenu, IntVar, Scale
)

def flatten_pdf():
    input_pdf = filedialog.askopenfilename(
        title="PDF파일 선택",
        filetypes=[("PDF파일", "*.pdf")]
    )
    if not input_pdf:
        return

    base, ext = os.path.splitext(input_pdf)
    output_pdf = base + "_image.pdf"

    try:
        dpi = int(dpi_var.get())
        quality = int(quality_var.get())

        doc = fitz.open(input_pdf)
        pil_images = []

        for page in doc:
            pix = page.get_pixmap(dpi=dpi, colorspace=fitz.csRGB)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            pil_images.append(img)

        pil_images[0].save(
            output_pdf,
            save_all=True,
            append_images=pil_images[1:],
            quality=quality,
            optimize=True
        )

        messagebox.showinfo("성공", f"결과 PDF 파일:\n{output_pdf}")

    except Exception as e:
        messagebox.showerror("오류!", str(e))


def show_about():
    about_text = (
"PDF 파일을 폰트 파일이 없는\n"
"이미지 PDF로 변환합니다.\n"
"Converts PDF files into image-only PDFs\n"
"without embedded font data.\n\n"

"제작자/Author: robocat00\n"
"소스코드/Source:\n"
"https://github.com/robocat00/PDF2ImagePDF3\n\n"

"라이선스/License:\n"
"GNU Affero General Public License v3.0 (AGPL-3.0)\n\n"

"본 프로그램은 AGPL 라이선스의\n"
"PyMuPDF (fitz) 모듈을 사용하므로\n"
"전체 소스코드는 AGPL로 공개되어야 합니다.\n"

"This program uses the AGPL-licensed\n"
"PyMuPDF (fitz) module, therefore\n"
"the entire source code must be released under the AGPL.\n\n"

"사용된 주요 모듈:\n"
"Main modules used:\n"
"- PyMuPDF (AGPL)\n"
"- Pillow (PIL / MIT License)\n"
    )
    
    messagebox.showinfo("정보 / About", about_text)


# --- GUI ---
root = Tk()
root.title("PDF2ImagePDF3")
root.geometry("350x300")

Label(root, text="PDF파일을 폰트없는 이미지형 PDF로 변환", font=("Arial", 12)).pack(pady=5)

dpi_var = StringVar(value="150")
Label(root, text="DPI선택(높을수록 고품질/고용량):").pack()
OptionMenu(root, dpi_var, "72", "150", "300").pack(pady=5)

Label(root, text="이미지화질 선택(높을수록 고품질/고용량):(0-100)").pack()
quality_var = IntVar(value=80)
Scale(root, from_=10, to=100, orient="horizontal",
      variable=quality_var).pack(pady=5)

Button(
    root,
    text="변환할 PDF파일 선택",
    command=flatten_pdf,
    width=25
).pack(pady=10)

Button(
    root,
    text="정보 / About",
    command=show_about,
    width=25
).pack(pady=5)

root.mainloop()
