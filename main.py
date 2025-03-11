from imposer import Imposer
from argparse import ArgumentParser, REMAINDER

if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument(
        "-c",
        "--combine",
        help="Combine different PDF files onto one. Consumes all passed parameters. Last one will me used as output.",
        action="store_true",
    )
    parser.add_argument(
        "-f",
        "--fill",
        help="Add blank pages to the end of the PDF file until the number of pages is divisible by four.",
        action="store_true",
    )
    parser.add_argument(
        "-i", "--impose", help="Impose a single PDF file.", action="store_true"
    )
    parser.add_argument(
        "-s",
        "--split",
        help="Takes a number n and splits a PDF file into signatures n-pages long. Default value is 32.",
        nargs="?",
        default=32,
        type=int,
    )
    parser.add_argument("files", nargs=REMAINDER)

    args = parser.parse_args()

    if args.combine:
        Imposer.combine(args.files)
    elif args.fill:
        for file in args.files:
            Imposer(file).fill()
    elif args.impose:
        for file in args.files:
            Imposer(file).impose()
    elif args.split:
        print(args)
        for file in args.files:
            Imposer(file).split(args.split)
    else:
        print("No actions were selected.")
