from pathlib import Path
from natsort import natsorted
from pikepdf import Pdf, Page, Rectangle

class Imposer:
    def __init__(self, path):
        working_file = Path(path)
        if working_file.exists() and working_file.suffix == ".pdf":
            self.file_path = working_file
        else:
            print(f"--File {working_file.name} is not a PDF file or does not exist.")

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
        ----> NOT WORKING
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

    def impose(self):
        pass

    def split(self, signature_length):
        '''

        file = um arquivo pdf a ser dividido
        signature_length = comprimento dos cadernos em páginas

        Divide um pdf em arquivos com um número fixo de páginas.
        '''

        filename = self.file_path.stem
        pdf = Pdf.open(self.file_path)
        document_pages = len(pdf.pages)

        # Check if number of pages on working document can be perfectly divided
        # by the provided signature length. i.e. 128 pages divided by 32-pages long
        # signatures will provide four evenly sized signatures.
        # If not the case, add another signature to contain the remaining pages.
        if document_pages % signature_length == 0:
            signatures = int(document_pages / signature_length)
        else:
            signatures = int(document_pages / signature_length) + 1
            print(f"--Number of document pages not a multiple of {signature_length}")
            print(f"--Last signature will contain {document_pages % signature_length} pages")

        Path(f"{filename}_split").mkdir(parents = True, exist_ok = True)
        print(f"--Number of pages on original file: {document_pages}")
        print(f"--Number of necessary signatures: {signatures}")

        for i in range(signatures):
            output = Pdf.new()
            start = i * signature_length
            stop = (i + 1) * signature_length
            print(f"--Exporting signature {i} containing pages {start} to {stop}")
            output.pages.extend(pdf.pages[start:stop])
            output.save(f"{filename}_split/{filename}_split_{i}.pdf")
