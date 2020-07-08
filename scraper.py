# Please read the README.md For Every Information
# python scraper.py --dlno DL-0420110149646 --dob 09-02-1976
import argparse
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import json

if __name__ == "__main__":
    # print("Please Enter Driving License Number (--dlno) , Date Of Birth (--dob)")
    # print("Using Flags Followed By A Space")
    parser = argparse.ArgumentParser()
    parser.add_argument("--dlno", metavar='', required=True, help="Driving License Number")
    parser.add_argument("--dob", metavar='', required=True, help="Date Of Birth")
    #    parser.add_argument("-C", "-captcha", metavar='', required=True, help="CAPTCHA")
    args = parser.parse_args()


    def get_captcha():
        return input(" Please Enter Captcha Manually From Browser ")


    chrome_browser = webdriver.Chrome('chromedriver.exe')
    chrome_browser.maximize_window()
    chrome_browser.get('https://parivahan.gov.in/rcdlstatus/?pur_cd=101')
    time.sleep(0.3)
    driving_license_number = chrome_browser.find_element_by_name('form_rcdl:tf_dlNO')
    driving_license_number.send_keys(args.dlno)

    dob = chrome_browser.find_element_by_name('form_rcdl:tf_dob_input')
    dob.send_keys(args.dob)
    chrome_browser.find_element_by_id('form_rcdl:j_idt15').click()

    captcha = chrome_browser.find_element_by_id('form_rcdl:j_idt32:CaptchaID').send_keys(get_captcha())
    print(' Please Wait! Validating Captcha ')
    check_status = chrome_browser.find_element_by_id('form_rcdl:j_idt43')
    check_status.click()
    time.sleep(3)
    time.sleep(3)

    ok = chrome_browser.find_elements_by_xpath("//*[@id='form_rcdl:j_idt13']/div/ul/li/span[2]")
    while bool(ok):
        cap_click = chrome_browser.find_element_by_id('form_rcdl:j_idt32:CaptchaID')
        chrome_browser.maximize_window()
        cap_click.clear()
        new_captcha = chrome_browser.find_element_by_id('form_rcdl:j_idt32:CaptchaID').send_keys(get_captcha())

        check_status = chrome_browser.find_element_by_id('form_rcdl:j_idt43')
        check_status.click()
        print(' Please Wait! Validating Captcha Again')
        time.sleep(3)
        ok = chrome_browser.find_elements_by_xpath("//*[@id='form_rcdl:j_idt13']/div/ul/li/span[2]")
        if bool(ok):
            continue
        else:
            break
    chrome_browser.minimize_window()
    print(" Verification Successful ")
    print(" Validated , Processing Information Now ")
    # png = chrome_browser.save_screenshot("status.png")
    chrome_browser.implicitly_wait(5)
    chrome_browser.implicitly_wait(5)
    with open("page_source.html", "w") as f:
        f.write(chrome_browser.page_source)

    with open("page_source.html", "r") as f:
        doc = BeautifulSoup(f, "html.parser")
        det = doc.select('tr')
        details = []
        for column, data in enumerate(det):
            detail = det[column].getText()
            details.append(detail)

        name1 = str(details[0])
        status_holder = name1.splitlines(keepends=False)
        sta_temp = str(status_holder[2])
        current_status = sta_temp

        name2 = str(details[1])
        status_holder = name2.splitlines(keepends=False)
        sta_temp = str(status_holder[2])
        applicant_name = sta_temp.replace(' ', '')

        name3 = str(details[3])
        temp = name3.splitlines(keepends=False)
        sta_temp = str(temp[2])
        last_txn_at = sta_temp

        name4 = str(details[4])
        temp = name4.splitlines(keepends=False)
        sta_temp = str(temp[2])
        old_or_new_dl_no = sta_temp

        name5 = str(details[5])
        temp = name5.splitlines(keepends=False)
        transport_type = str(temp[1])
        validity_from = str(temp[2]).split()
        validity_upto = str(temp[3]).split()

        name6 = str(details[6])
        temp = name6.splitlines(keepends=False)
        transport = str(temp[1])
        from_where = str(temp[2]).split()
        upto_where = str(temp[3]).split()

        name7 = str(details[7])
        temp = name7.splitlines(keepends=False)
        hazardous_valid_till = str(temp[2])
        hill_valid_till = str(temp[4])

        class_of_vechile = str(details[9])

        data = {'Details': []}
        data['Details'].append({
            'Current Status : ': current_status,
            'Date Of Birth : ': args.dob,
            'Applicant Name : ': applicant_name,
            'Last Transaction At : ': last_txn_at,
            'Old/New DL Number : ': old_or_new_dl_no,
            'Transport Type : ': transport_type,
            'Validity From : ': validity_from[1],
            'Validity Upto : ': validity_upto[1],
            'Transport : ': transport,
            'From : ': from_where[1],
            'To : ': upto_where[1],
            'Hazardous Valid Till : ': hazardous_valid_till,
            'Hill Valid Till : ': hill_valid_till,
            'Class Of Vehicle : ': class_of_vechile,
        })

        with open('data.json', 'w') as outfile:
            json.dump(data, outfile)

        chrome_browser.close()
        print(' Done Extracted And Exported To .json File ')
