import os
from raiffeisen_parser import parse_pdf
from excel_writer import save_excel


INPUT_FOLDER = "input"
OUTPUT_FOLDER = "output"


def main():

    os.makedirs(INPUT_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)


    pdf_files = [
        f for f in os.listdir(INPUT_FOLDER)
        if f.lower().endswith(".pdf")
    ]


    if not pdf_files:
        print("Nincs PDF az input mappában.")
        return


    all_transactions = []


    for pdf in pdf_files:

        filepath = os.path.join(
            INPUT_FOLDER,
            pdf
        )

        print("Feldolgozás:", pdf)

        all_transactions.extend(
            parse_pdf(filepath)
        )


    save_excel(
        all_transactions,
        os.path.join(
            OUTPUT_FOLDER,
            "Raiffeisen_kivonat.xlsx"
        )
    )


if __name__ == "__main__":
    main()
