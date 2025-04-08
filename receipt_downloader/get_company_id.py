from __future__ import print_function
import fattureincloud_python_sdk as fc

def get_company_id(configuration):
    with fc.ApiClient(configuration) as api_client:
        api_instance = fc.UserApi(api_client)

        try:
            api_response = api_instance.list_user_companies()
            company_id = api_response.data.companies[0].id

            print("Company ID ottenuto con successo.")
        except fc.ApiException as e:
            print(f"Errore durante l'ottenimento del company id: ${e}")
    
    return company_id