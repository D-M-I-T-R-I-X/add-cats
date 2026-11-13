import json
import requests


GROUP_NAME = "PYAPI-162"
TOKEN = ""
CATAAS_URL = "https://cataas.com/cat/cute/says"
DISK_URL = "https://cloud-api.yandex.net/v1/disk/resources"
TIMEOUT = 30


def download_cat(text):
    # Формируем адрес  с текстом
    encoded_text = requests.utils.quote(text, safe="")
    response = requests.get(
        f"{CATAAS_URL}/{encoded_text}", params={"format": "png"}, timeout=TIMEOUT
    )
    return response.content


def create_folder(folder, headers):
    # Создаем папку группы
    requests.put(DISK_URL, headers=headers, params={"path": folder}, timeout=TIMEOUT)


def upload_file(path, image, headers):
    # Получаем ссылку и загружаем по ней картинку
    response = requests.get(
        f"{DISK_URL}/upload",
        headers=headers,
        params={"path": path, "overwrite": "false"},
        timeout=TIMEOUT,
    )
    upload_url = response.json()["href"]
    requests.put(upload_url, data=image, timeout=TIMEOUT)



def main():
    text = input("Текст для картинки: ").strip()
    headers = {"Authorization": f"OAuth {TOKEN}"}
    folder = f"disk:/{GROUP_NAME}"
    image = download_cat(text)
    file_name = text + ".png"
    create_folder(folder, headers)
    upload_file(f"{folder}/{file_name}", image, headers)

    # Формируем и сохраняем json
    report = [{"file_name": file_name, "size": len(image)}]
    with open("result.json", "w", encoding="utf-8") as file:
        json.dump(report, file, ensure_ascii=False, indent=2)
        file.write("\n")


main()
