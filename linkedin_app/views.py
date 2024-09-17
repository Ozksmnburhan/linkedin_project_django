from django.shortcuts import render, redirect
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def linkedin_login_and_scrape(request):
    if request.method == "POST":
        linkedin_username = request.POST.get("linkedin_username")
        linkedin_password = request.POST.get("linkedin_password")
        company_name = request.POST.get("company_name")

        from selenium.webdriver.chrome.options import Options

        options = Options()
        options.add_argument("--headless")  # Headless mode kullanımı
        options.add_argument("--no-sandbox")  # Güvenlik nedeniyle bazı sunucularda gerekli olabilir
        options.add_argument("--disable-dev-shm-usage")  # Bellek kullanımını optimize eder

        driver = webdriver.Chrome(options=options)

        # LinkedIn login fonksiyonu
        driver.get('https://www.linkedin.com/login')
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'username')))
        username_input = driver.find_element(By.ID, 'username')
        password_input = driver.find_element(By.ID, 'password')
        username_input.send_keys(linkedin_username)
        password_input.send_keys(linkedin_password)
        password_input.send_keys(Keys.RETURN)

        # Şirket sayfasına gidip bilgi çekme
        company_url = f"https://www.linkedin.com/company/{company_name.lower()}/about/"
        driver.get(company_url)
        WebDriverWait(driver, 20).until(lambda d: d.execute_script('return document.readyState') == 'complete')

        # Şirket bilgilerini burada alabilirsiniz.
        company_info = {
            "Name": company_name,
            "URL": company_url,
            "Description": driver.find_element(By.CSS_SELECTOR, 'section.artdeco-card p.break-words').text
        }

        driver.quit()

        return render(request, "linkedin_app/index.html", {"company_info": company_info})

    return render(request, "linkedin_app/index.html")
