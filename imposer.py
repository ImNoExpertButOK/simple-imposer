from pathlib import Path
from natsort import natsorted
from pikepdf import Pdf, Page, Rectangle


class Imposer:
    def __init__(self, path):
        if Path(path).exists():
            self.file_path = Path(path)
        else:
            print("--File is not a PDF file or does not exist.")

    def fill(self):
        '''
        Verifica o número de páginas de um PDF e
        preenche com páginas brancas até ser divisível por 4.
        Modifies file in place!
        '''

        with Pdf.open(self.file_path, allow_overwriting_input=True) as pdf:
            print(f"--Name of file: {self.file_path.name}")
            print(f"--Number of pages on file: {len(pdf.pages)}")

            # Get the cropbox of the document, in points.
            dimensions = pdf.pages[0].cropbox.as_list()

            # Dimensions are of class decimal, but needs to be cast as
            # float when passed to the add_blank_page method.
            width = float(dimensions[2])
            height = float(dimensions[3])

            if len(pdf.pages) % 4 != 0:
                print("--Number of pages not divisible by four. Filling up until divisible.")
                while len(pdf.pages) % 4 != 0:
                    pdf.add_blank_page(page_size=(width, height))
                pdf.save(self.file_path)
            else:
                print("--Number of pages is already a multiple of four.")

    def combine(self):
        '''
        Combines multiple PDF files into one.
        '''

        output = Pdf.new()
        print("--Combinando os seguintes PDFs encontrados:")
        for file in natsorted(Path(path).glob("*.pdf")):
            print(file.name)
            src = Pdf.open(file)
            output.pages.extend(src.pages)
        print("--Gerando arquivo final")
        output.save("combined_output.pdf")
