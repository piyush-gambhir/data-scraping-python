from docx2pdf import convert
from pdf2docx import Converter

def convert_word_to_pdf_docx2pdf(input_file, output_file):
    convert(input_file, output_file)

def convert_word_to_pdf_pdf2docx(input_file, output_file):
    cv = Converter(input_file)
    cv.convert(output_file, start=0, end=None)
    cv.close()

