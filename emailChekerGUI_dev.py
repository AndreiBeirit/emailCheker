import json
import base64
import requests
import tkinter as tk
import customtkinter
import pymysql
from db_creds2 import db_host, db_port, db_user, db_password, db_name, ssh_ip, ssh_port, ssh_username, ssh_password

db_host = db_host
db_port = db_port
db_name = db_name
db_user = db_user
db_password = db_password

product_version = "DEV"

root = customtkinter.CTk()
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")
root.geometry("600x280")
root.resizable(False, False)
root.title(f"Для теребоньки почты_{product_version}")

email_label = customtkinter.CTkLabel(root, text="Введите Email от Battle.net аккаунта:")
email_label.pack(pady=5)
email_entry = customtkinter.CTkEntry(root, width=250)
email_entry.pack(pady=5)

info_text = customtkinter.CTkTextbox(root, height=100, width=500)
info_text.pack(pady=20)

def get_email_password(email):
    connection = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name, port=db_port)

    cursor = connection.cursor()

    # просим пароль
    query = f"SELECT EmailPassword FROM Accounts WHERE Email='{email}'"
    cursor.execute(query)
    result = cursor.fetchone()
    
    # тушим коннект
    cursor.close()
    connection.close()
    # ssh.close()
    
    if result:
        return result[0]
    else:
        return None

def send_request():
    info_text.delete(1.0, tk.END)
    url = "https://i/blizzard/getverifcode"
    email = email_entry.get().strip()

    if not (len(email.replace(' ', '').replace('\t', '')) > 0 and len(email) <= 40):
        info_text.insert(tk.END, "Email не может быть пустым\n", "error")
        return

    email_password = get_email_password(email)

    if not email_password:
        info_text.insert(tk.END, "Email не найден\n", "error")
        return
    
    payload = {'Email': email, 'Password': email_password}
    headers = {
        "Authorization": f"Basic {base64.b64encode('imap-user:Ltylhfhbev123~'.encode()).decode()}",
        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8"
    }

    response = requests.post(url, headers=headers, data=payload)
    response_error = json.loads(response.text)
    error_value = response_error['response']

    if response.status_code == 200:
        pass
    else:
        info_text.insert(tk.END, f'{error_value}\n')
        return
    
    try:
        response_data = json.loads(response.text)
        code_value = response_data['code']
        info_text.insert(tk.END, f"Код разблокировки аккаунта Battle.net: {code_value}\n")
    except KeyError:
        return

send_button = customtkinter.CTkButton(root, text="Отправить", command=send_request)
send_button.pack(pady=10)

root.mainloop()
