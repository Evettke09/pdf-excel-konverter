import pdfplumber
import re


def clean_amount(value):

    if not value:
        return None

    value = (
        value
        .replace(".", "")
        .replace(",", ".")
        .replace(" ", "")
    )

    try:
        return float(value)

    except:
        return None



def is_date(line):

    return bool(
        re.match(
            r"^\d{4}\.\d{2}\.\d{2}",
            line
        )
    )



def find_account_number(text):

    match = re.search(
        r"\d{3,8}[- ]\d{3,8}[- ]\d{3,8}",
        text
    )

    if match:
        return match.group()

    return ""



def parse_pdf(pdf_path):

    transactions = []


    with pdfplumber.open(pdf_path) as pdf:


        for page in pdf.pages:


            text = page.extract_text()


            if not text:
                continue


            lines = [
                x.strip()
                for x in text.split("\n")
                if x.strip()
            ]


            current = None


            for line in lines:


                if is_date(line):


                    if current:
                        transactions.append(current)


                    current = {

                        "Dátum": "",
                        "Értéknap": "",
                        "Tranzakció típusa": "",
                        "Partner": "",
                        "Bankszámlaszám": "",
                        "Közlemény": "",
                        "Összeg": None

                    }


                    parts = line.split()


                    current["Dátum"] = parts[0]


                    if len(parts) > 1:
                        current["Értéknap"] = parts[1]


                    # összeg keresés
                    amounts = re.findall(
                        r"-?\d+\.\d+,\d{2}",
                        line
                    )


                    if amounts:

                        current["Összeg"] = clean_amount(
                            amounts[-1]
                        )



                elif current:


                    # tranzakció típus
                    if not current["Tranzakció típusa"]:

                        current["Tranzakció típusa"] = line



                    # bankszámlaszám
                    account = find_account_number(line)

                    if account:

                        current["Bankszámlaszám"] = account



                    # partner
                    elif not current["Partner"]:

                        current["Partner"] = line



                    # közlemény
                    else:

                        current["Közlemény"] += (
                            " " + line
                        )



            if current:
                transactions.append(current)


    return transactions
