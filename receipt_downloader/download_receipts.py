from __future__ import print_function
import json
import requests
import certifi
import fattureincloud_python_sdk as fc
from fattureincloud_python_sdk.api import IssuedDocumentsApi
from fattureincloud_python_sdk.models.email_schedule import EmailSchedule
from fattureincloud_python_sdk.models.schedule_email_request import ScheduleEmailRequest
from receipt_downloader.config_receipt import config_receipt
from config import COMPANY_ID, ACCESS_TOKEN

def download_receipt(receipt_data, idx):
    with open("files/receipt_template.json", "r") as file:
        receipt_template = json.load(file)

    configuration = fc.Configuration(
        host = "https://api-v2.fattureincloud.it",
        access_token=ACCESS_TOKEN,
        ssl_ca_cert=certifi.where()
    )

    company_id = COMPANY_ID

    data = config_receipt(receipt_template, receipt_data["name"], receipt_data["subject"], receipt_data["date"], float(receipt_data["amount"]))

    receipt_response = create_receipt(configuration, company_id, data)

    download_receipt_pdf(configuration, company_id, receipt_response.data.id, f"receipts/receipt_{idx+1}.pdf")

    # send_email(configuration, company_id, receipt_response.data.id)


def create_receipt(configuration, company_id, receipt_data):
    with fc.ApiClient(configuration) as api_client:
        issued_documents_api = IssuedDocumentsApi(api_client)

        try:
            response = issued_documents_api.create_issued_document(company_id, receipt_data)

            if __name__ == "__main__":
                print(f'Ricevuta creata con successo. ID: {response.data.id}')

            return response

        except fc.ApiException as e:
            print(f"Errore durante la creazione della ricevuta: {e}")

def download_receipt_pdf(configuration, company_id, receipt_id, file_path):
    with fc.ApiClient(configuration) as api_client:
        api_instance = fc.IssuedDocumentsApi(api_client)
        try:
            document = api_instance.get_issued_document(company_id, receipt_id)

            pdf_url = document.data.url
            
            response = requests.get(pdf_url)
            response.raise_for_status()  # Raise an exception for HTTP errors
            
            # Save the PDF to a local file
            with open(file_path, 'wb') as pdf_file:
                pdf_file.write(response.content)
            
            print(f"Ricevuta {receipt_id} salvata con successo in: {file_path}")
        except Exception as e:
            print(f"Errore durante il salvataggio della ricevuta: {e}")

def send_email(configuration, company_id, receipt_id):
    email = EmailSchedule(
        sender_id=0,
        recipient_email="lorenzobunaj@gmail.com",
        subject=f"RICEVUTA FIC {receipt_id}",
        body=f"Ricevuta Fattureincloud ID: {receipt_id}",
        include=fc.EmailScheduleInclude(
            document=True,
            delivery_note=False,
            attachment=False,
            accompanying_invoice=False
        ),
        attach_pdf=True,
        send_copy=False
    )

    schedule_email_request = ScheduleEmailRequest(
        data = email
    )

    with fc.ApiClient(configuration) as api_client:

        api_instance = IssuedDocumentsApi(api_client)
        try:
            api_instance.schedule_email(company_id, receipt_id, schedule_email_request=schedule_email_request)

            if __name__ == "__main__":
                print(f"Email inviata con successo.")
        except fc.ApiException as e:
            print(f"Errore durante l'invio della mail: {e}")