import json
import base64
import requests
import tkinter as tk
import customtkinter

product_version = "2.1"

root = customtkinter.CTk()
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")
root.geometry("600x370")
root.resizable(False, False)
root.title(f"Получение кода разблокировки аккаунтов_v{product_version}")

email_label = customtkinter.CTkLabel(root, text="Введите Email от Battle.net/Steam аккаунта:")
email_label.pack(pady=5)
email_entry = customtkinter.CTkEntry(root, width=250)
email_entry.pack(pady=5)

password_label = customtkinter.CTkLabel(root, text="Введите пароль от email:")
password_label.pack(pady=5)
password_entry = customtkinter.CTkEntry(root, width=250, show="*")
password_entry.pack(pady=5)
show_password = customtkinter.BooleanVar()

def toggle_password_visibility():
    if show_password.get():
        password_entry.configure(show="")
    else:
        password_entry.configure(show="*") 

password_checkbox = customtkinter.CTkCheckBox(root, text="Показать пароль", variable=show_password, command=toggle_password_visibility)
password_checkbox.pack(pady=5)  

info_text = customtkinter.CTkTextbox(root, height=100, width=500)
info_text.pack(pady=15)    

def send_request_bnet():
    info_text.delete(1.0, tk.END)
    url = "https://i/blizzard/getverifcode"
    email = email_entry.get().strip()
    password = password_entry.get().replace(' ', '').replace('\t', '')

    if not (len(email.replace(' ', '').replace('\t', '')) > 0 and len(email) <= 40):
        info_text.insert(tk.END, "Email не может быть пустым\n", "error")
        return

    elif not (len(password) > 0 and len(password) <= 40):
        info_text.insert(tk.END, "Пароль не может быть пустым\n", "error")
        return

    headers = {
        "Authorization": f"Basic {base64.b64encode('imap-user:Ltylhfhbev123~'.encode()).decode()}",
        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8"
    }

    payload = {'Email': email, 'Password': password}

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
        info_text.insert(tk.END, f"Код разблокировки аккаунта: {code_value}\n")
    except KeyError:
        return

def send_request_steam():
    info_text.delete(1.0, tk.END)
    url = "https://i/steam/getverifcode"
    email = email_entry.get().strip()
    password = password_entry.get().replace(' ', '').replace('\t', '')

    if not (len(email.replace(' ', '').replace('\t', '')) > 0 and len(email) <= 40):
        info_text.insert(tk.END, "Email не может быть пустым\n", "error")
        return

    elif not (len(password) > 0 and len(password) <= 40):
        info_text.insert(tk.END, "Пароль не может быть пустым\n", "error")
        return

    headers = {
        "Authorization": f"Basic {base64.b64encode('imap-user:Ltylhfhbev123~'.encode()).decode()}",
        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8"
    }

    payload = {'Email': email, 'Password': password}

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
        info_text.insert(tk.END, f"Код разблокировки аккаунта: {code_value}\n")
    except KeyError:
        return 

button_frame = customtkinter.CTkFrame(root)
button_frame.pack(pady=5)

send_button_bnet = customtkinter.CTkButton(button_frame, text="Battle.net", command=send_request_bnet)
send_button_bnet.pack(side=tk.LEFT, padx=5)

send_button_steam = customtkinter.CTkButton(button_frame, text="Steam", command=send_request_steam)
send_button_steam.pack(side=tk.LEFT, padx=5)

root.mainloop()
