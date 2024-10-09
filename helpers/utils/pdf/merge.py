from PyPDF2 import PdfWriter


def merge_pdfs(input_files, output_file):
    merger = PdfWriter()

    for pdf in input_files:
        merger.append(pdf)

    merger.write(output_file)
    merger.close()


