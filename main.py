import csv
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


def get_data(url) -> list:
    browser_options = ChromeOptions()
    browser_options.headless = True
    browser_options.add_argument("--window-size=1920,1080")
    browser_options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    )
    
    driver = Chrome(options=browser_options)
    driver.get(url)
    action_chains = ActionChains(driver)
    
    data = []
    
    # ambil button next
    next_button = driver.find_element(By.CLASS_NAME, "c-page-link-next")
    # Eksekusi JavaScript untuk mengklik elemen
    # driver.execute_script("arguments[0].click();", next_button)        
    
    # Loop untuk mengambil data dari setiap halaman
    while True:
        # Identifikasi elemen <tr> yang tidak memiliki atribut class
        rows = driver.find_elements(By.XPATH, "//table//tr[not(@class)]")

        # Loop melalui setiap elemen <tr>
        for row in rows:
            # List untuk menyimpan data dalam satu baris
            row_data = []
            
            # Identifikasi elemen <td> dalam setiap elemen <tr>
            cells = row.find_elements(By.XPATH, ".//td")

            # Loop melalui setiap elemen <td>
            for cell in cells:
                # Ambil teks dari elemen <td>
                text = cell.text.replace('\n', ' ')
                row_data.append(text)
            
            data.append(row_data)
        
        
        
        next_button = driver.find_element(By.XPATH, "//a[@aria-label='Next page']")
        # Periksa atribut 'aria-disabled'
        disabled = next_button.get_attribute("aria-disabled")
        if disabled == "true":
            break  # Hentikan looping jika disabled = true
        
        # Klik tombol "next" menggunakan JavaScript
        driver.execute_script("arguments[0].click();", next_button)

    driver.quit()
    return data


def main():
    data = get_data("https://ppdb.jabarprov.go.id/wilayah_ppdb/cadisdik/KOTA%20BOGOR/info-pendaftar/20220332")
    # Nama file CSV
    filename = "data.csv"
    
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)
        
    # print(data)


if __name__ == '__main__':
    main()