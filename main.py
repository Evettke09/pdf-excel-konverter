import os
from raiffeisen_parser import parse_pdf
from excel_writer import save_excel


INPUT_FOLDER = "input"
OUTPUT_FOLDER = "output"


def main():

    if not os.path.exists(INPUT_FOLDER):
        os.makedirs(INPUT_FOLDER)

    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)


    pdf_files = [
        f for f in os.listdir(INPUT_FOLDER)
        if f.lower().endswith(".pdf")
    ]


    if not pdf_files:
        print("Nincs PDF az input mappában.")
        return


    all_transactions = []


    for pdf_file in pdf_files:

        path = os.path.join(INPUT_FOLDER, pdf_file)

        print(f"Feldolgozás: {pdf_file}")

        transactions = parse_pdf(path)

        all_transactions.extend(transactions)


    save_excel(
        all_transactions,
        os.path.join(
            OUTPUT_FOLDER,
            "Raiffeisen_kivonat.xlsx"
        )
    )


    print("Kész! Az Excel elkészült.")



if __name__ == "__main__":
    main()
