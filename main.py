from receipt_downloader.download_receipts import download_receipt
import pandas as pd
import subprocess

merge_pdfs = "merge_pdf.js"

def main():
    file_path = 'files/ricavi_istituzionali.csv'

    df = pd.read_csv(file_path)

    receipts_data = []
    for index, row in df.iterrows():
        receipts_data.append(row.to_dict())
    # print(receipts_data)

    receipts_list = []
    for (i, r) in enumerate(receipts_data):
        if (r["receipt"] == 'YES'):
            download_receipt(r,i)

            if (i % 5 == 0):
                input("continue? ")

    '''
    try:
        result = subprocess.run(["node", merge_pdfs], check=True, capture_output=True, text=True)

        print("Output from Node.js:")
        print(result.stdout)

    except subprocess.CalledProcessError as e:
        print("Error running the JavaScript file:")
        print(e.stderr)
    '''

    

if __name__ == "__main__":
    main()