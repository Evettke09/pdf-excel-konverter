import pdfplumber


PDF_FILE = "input/teszt.pdf"


def main():

    with pdfplumber.open(PDF_FILE) as pdf:

        for page_number, page in enumerate(pdf.pages, start=1):

            print("\n" + "=" * 80)
            print(f"OLDAL: {page_number}")
            print("=" * 80)


            text = page.extract_text()


            if text:

                lines = text.split("\n")


                for i, line in enumerate(lines, start=1):

                    print(
                        f"{i:03d}: {line}"
                    )

            else:

                print("Nem talált szöveget az oldalon.")



if __name__ == "__main__":
    main()
