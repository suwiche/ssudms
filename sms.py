from datetime import datetime
import requests


def get_data():
    date_time = datetime.now();
    types = ["cso", "cdc", "cdw", "swda", "swmcc", "pmc", "scc", "ps"]
    response = requests.get("http://127.0.0.1:8000/dashboard/update_sms/")
    response_data = response.json()
    message = ""
    for row in types:
        if row != "swda":
            message = message + "\n" + '{} near to expire and {} expired for {} Accreditation, '.format(
                response_data['data'][row]['accreditation']['near'],
                response_data['data'][row]['accreditation']['expired'], row)
            for i in response_data['data'][row]['accreditation']['contact_person']:
                if i['status'] == "near" and i['cellphone_no']:
                    send_sms("Sample Only! Hi, As of {} your Accreditation is nearly to expire.".format(
                        date_time.strftime("%B %d, %Y")), i['cellphone_no'])
                elif i['status'] == "expired" and i['cellphone_no']:
                    send_sms("Sample Only! Hi, As of {} your Accreditation is expired.".format(
                        date_time.strftime("%B %d, %Y")), i['cellphone_no'])
        elif row == "swda":
            message = message + "\n" + '{} near to expire and {} expired for {} Registration, '.format(
                response_data['data'][row]['registration']['near'],
                response_data['data'][row]['registration']['expired'], row)
            for i in response_data['data'][row]['registration']['contact_person']:
                if i['status'] == "near" and i['cellphone_no']:
                    send_sms("Sample Only! Hi, As of {} your Registration is nearly to expire.".format(
                        date_time.strftime("%B %d, %Y")), i['cellphone_no'])
                elif i['status'] == "expired" and i['cellphone_no']:
                    send_sms("Sample Only! Hi, As of {} your Registration is expired.".format(
                        date_time.strftime("%B %d, %Y")), i['cellphone_no'])

            message = message + "\n" + '{} near to expire and {} expired for {} Licensing, '.format(
                response_data['data'][row]['licensing']['near'], response_data['data'][row]['licensing']['expired'],
                row)
            for i in response_data['data'][row]['licensing']['contact_person']:
                if i['status'] == "near" and i['cellphone_no']:
                    send_sms("Sample Only! Hi, As of {} your License is nearly to expire.".format(
                        date_time.strftime("%B %d, %Y")), i['cellphone_no'])
                elif i['status'] == "expired" and i['cellphone_no']:
                    send_sms(
                        "Sample Only! Hi, As of {} your License is expired.".format(date_time.strftime("%B %d, %Y")),
                        i['cellphone_no'])

            message = message + "\n" + '{} near to expire and {} expired for {} Accreditation, '.format(
                response_data['data'][row]['accreditation']['near'],
                response_data['data'][row]['accreditation']['expired'], row)
            for i in response_data['data'][row]['accreditation']['contact_person']:
                if i['status'] == "near" and i['cellphone_no']:
                    send_sms("Sample Only! Hi, As of {} your Accreditation is nearly to expire.".format(
                        date_time.strftime("%B %d, %Y")), i['cellphone_no'])
                elif i['status'] == "expired" and i['cellphone_no']:
                    send_sms("Sample Only! Hi, As of {} your Accreditation is expired.".format(
                        date_time.strftime("%B %d, %Y")), i['cellphone_no'])

    message = 'As of {}, there are {}'.format(date_time.strftime("%B %d, %Y"), message)
    send_sms(message, "09356207449")
    print('Sms Successfully sent.')


def send_sms(message, number):
    token_auth = 'Token 94f1eabd887dee4ace64ab417df3413a98d9a6c9'
    headers = {"Authorization": token_auth}
    response = requests.post(
        "https://caraga-portal.dswd.gov.ph/api/send-message/?id_number=16-12188&message={}&number={}".format(message,
                                                                                                             number),
        headers=headers)
    response_data = response.json()


get_data()
