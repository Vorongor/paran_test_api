from fpdf import FPDF
from io import BytesIO

from pdf_service.schemas import UserReadSchema


def generate_user_pdf(user: UserReadSchema) -> bytes | bytearray| BytesIO:
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(40, 10, f"User Profile: {user.name} {user.surname}", ln=True)

    pdf.set_font("Arial", size=12)
    pdf.ln(10)

    pdf.cell(0, 10, f"ID: {user.id}", ln=True)
    pdf.cell(0, 10, f"Email: {user.email}", ln=True)
    pdf.cell(0, 10, f"Date of Birth: {user.date_of_birth}", ln=True)

    pdf_output = BytesIO()
    pdf_bytes = pdf.output()
    pdf_output.write(pdf_bytes)
    pdf_output.seek(0)

    return pdf_output
