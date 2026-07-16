import streamlit as st
import tempfile
import os

from raiffeisen_parser import parse_pdf
from excel_writer import save_excel


st.title("Raiffeisen PDF → Excel konverter")

uploaded_file = st.file_uploader(
    "Töltsd fel a Raiffeisen PDF kivonatot",
    type=["pdf"]
)


if uploaded_file:

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ) as tmp:

        tmp.write(
            uploaded_file.getbuffer()
        )

        pdf_path = tmp.name


    if st.button("Átalakítás Excelbe"):

        with st.spinner("Feldolgozás..."):

            transactions = parse_pdf(pdf_path)

            output_file = "Raiffeisen_kivonat.xlsx"

            save_excel(
                transactions,
                output_file
            )


            with open(
                output_file,
                "rb"
            ) as file:

                st.download_button(
                    label="Excel letöltése",
                    data=file,
                    file_name="Raiffeisen_kivonat.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )


    os.remove(pdf_path)
