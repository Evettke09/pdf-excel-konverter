import pdfplumber
import re
from datetime import datetime


def clean_amount(value):
    """
    Magyar formátumú összeg átalakítása számmá.
    Példa:
    -20.000,00 -> -20000.00
    """

    if not value:
        return None

    value = value.replace(" ", "")
    value = value.replace(".", "")
    value = value.replace(",", ".")

    try:
        return float(value)

    except:
        return None



def is_date(text):
    """
    Dátum felismerése
    Példa:
    2025.02.01
    """

    pattern = r"^\d{4}\.\d{2}\.\d{2}"

    return bool(
        re.match(pattern, text)
    )



def parse_pdf(pdf_path):

    transactions = []


    with pdfplumber.open(pdf_path) as pdf:


        for page in pdf.pages:

            text = page.extract_text()


            if not text:
                continue


            lines = text.split("\n")


            current = None


            for line in lines:


                line = line.strip()


                if not line:
                    continue



                # Új tranzakció kezdete
                if is_date(line):


                    # előző mentése
                    if current:
                        transactions.append(current)



                    current = {

                        "Dátum": "",
                        "Értéknap": "",
                        "Tranzakció típusa": "",
                        "Partner": "",
                        "Közlemény": "",
                        "Összeg": None,
                        "Egyenleg": None

                    }



                    parts = line.split()


                    current["Dátum"] = parts[0]


                    # számok keresése a sorban
                    numbers = []


                    for p in parts:

                        if re.search(
                            r"-?\d+\.\d+,\d{2}",
                            p
                        ):
                            numbers.append(p)



                    if numbers:

                        current["Összeg"] = clean_amount(
                            numbers[0]
                        )


                        if len(numbers) > 1:

                            current["Egyenleg"] = clean_amount(
                                numbers[-1]
                            )



                else:

                    if current is None:
                        continue



                    # összeg folytatás felismerése
                    amounts = re.findall(
                        r"-?\d+\.\d+,\d{2}",
                        line
                    )


                    if amounts:

                        current["Összeg"] = clean_amount(
                            amounts[0]
                        )


                    else:

                        # első szövegsor partner
                        if not current["Partner"]:

                            current["Partner"] = line

                        else:

                            current["Közlemény"] += (
                                " " + line
                            )



            if current:

                transactions.append(current)



    return transactions
