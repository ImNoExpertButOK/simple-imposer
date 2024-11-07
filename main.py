from imposer import Imposer
from argparse import ArgumentParser, REMAINDER

if __name__ == "__main__":

    parser = ArgumentParser()

    parser.add_argument("-c", "--combine", help="Combine different PDF files onto one.", action="store_true")
    parser.add_argument("-f", "--fill", help="Add blank pages to the end of the PDF file until the number of pages is divisible by four.", action="store_true")
    parser.add_argument("-i", "--impose", help="Impose a single PDF file.", action="store_true", default=False)
    parser.add_argument("-b", "--batch-impose", help="Impose multiple PDF files.", action="store_true")
    parser.add_argument("-s", "--split", help="Split a PDF file into signatures.", action="store_true")
    parser.add_argument("-d", "--directory", help="Path to a directory containing PDF files.", action="store_true")
    parser.add_argument("files", nargs=REMAINDER)

    args = parser.parse_args()

    if args.fill:
        for file in files:
        file = Imposer(files)

    # file = Imposer(file)
    # file.fill()
