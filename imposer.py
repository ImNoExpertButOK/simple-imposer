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

    def page_dimensions(self):
        """
        Get the cropbox of the document, in points.
        """

        # Get the cropbox of the document, in points.
        pdf = Pdf.open(self.file_path)
        dimensions = pdf.pages[0].cropbox.as_list()

        # Dimensions are of class decimal, but needs to be cast as
        # float when passed to the add_blank_page method.
        return float(dimensions[2]), float(dimensions[3])

    def fill(self):
        """
        Checks the number of pages on a file and fills it with blanks
        until it's divisible by four. Modifies file in place!
        """

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

    def impose(self):
        """
        A ideia desse algoritmo de imposição gira em
        torno do fato de que somados os números das páginas
        de cada spread após imposição, a soma sempre será o mesmo número.
        No caso, o número de páginas + 1. Por exemplo, em um caderno
        de 12 páginas, após imposição teria o seguinte esquema:
        12 | 01 -> 13
        02 | 11 -> 13
        10 | 03 -> 13
        04 | 09 -> 13
        08 | 05 -> 13
        06 | 07 -> 13
        Desta forma, o que o algoritmo faz é um loop de metade do
        número de páginas, aonde em cada volta ele subtrai o número
        da página atual do total + 1 para conseguir a disposição das páginas,
        e usa a boolean "switch" para alternar o lado em que são posicionadas,
        direita ou esquerda.
        """

        print("--Checking if file is file has an appropriate number of pages.")
        self.fill()

        with Pdf.open(self.file_path) as pdf:
            number_of_pages = len(pdf.pages)
            filename = self.file_path.stem
            total = number_of_pages + 1
            width, height = self.page_dimensions()

            output = Pdf.new()

            for i in range(1, int(number_of_pages / 2) + 1):

                output.add_blank_page(page_size=(width * 2, height))

                index = pdf.pages[i - 1]
                reverse_index = pdf.pages[total - i - 1]

                left_side_area = Rectangle(0, 0, width, height)
                right_side_area = Rectangle(width, 0, width * 2, height)

                dest_page = Page(output.pages[-1])  # ultima página criada

                if i % 2 == 0:
                    dest_page.add_overlay(pdf.pages[i - 1], left_side_area)
                    dest_page.add_overlay(pdf.pages[total - i - 1], right_side_area)
                    print("--Spread:", i, "-", total - i)
                else:
                    dest_page.add_overlay(pdf.pages[total - i - 1], left_side_area)
                    dest_page.add_overlay(pdf.pages[i - 1], right_side_area)
                    print("--Spread:", total - i, "-", i)

            print(f"--Saving file as {filename}_impo.pdf")
            output.save(f"{filename}_impo.pdf")

    def split(self, signature_length):
        """
        Splits a PDF file into signatures with the provided signature_length
        """

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

        Path(f"{filename}_split").mkdir(parents=True, exist_ok=True)
        print(f"--Number of pages on original file: {document_pages}")
        print(f"--Number of necessary signatures: {signatures}")

        for i in range(signatures):
            output = Pdf.new()
            start = i * signature_length
            stop = (i + 1) * signature_length
            print(f"--Exporting signature {i} containing pages {start} to {stop}")
            output.pages.extend(pdf.pages[start:stop])
            output.save(f"{filename}_split/{filename}_split_{i}.pdf")

    def combine(self, list_of_files):
        """
        ----> NOT WORKING
        Combines multiple PDF files into one.
        """

        output = Pdf.new()
        print("--Combining the following PDFs:")

        for file in natsorted(Path(path).glob("*.pdf")):
            print(file.name)
            src = Pdf.open(file)
            output.pages.extend(src.pages)
        print("--Gerando arquivo final")
        output.save("combined_output.pdf")
