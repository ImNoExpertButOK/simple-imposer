from imposer import Imposer
from argparse import ArgumentParser, REMAINDER

if __name__ == "__main__":

    parser = ArgumentParser()

    parser.add_argument("-c", "--combine", help="Combine different PDF files onto one.", action="store_true")
    parser.add_argument("-f", "--fill", help="Add blank pages to the end of the PDF file until the number of pages is divisible by four.", action="store_true")
    parser.add_argument("-i", "--impose", help="Impose a single PDF file.", action="store_true")
    parser.add_argument("-s", "--split", help="Takes a number n and splits a PDF file into signatures n-pages long. Default value is 32.", nargs="?", default=32, type=int)
    parser.add_argument("files", nargs=REMAINDER)

    args = parser.parse_args()

    for file in args.files:
        pdf = Imposer(file)
        pdf.impose()

        # pdf.split(args.split)

    # file = Imposer(file)
    # file.fill()
