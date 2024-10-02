import art 
print(art.text2art("Aphonia  AI"))


import os
from dotenv import load_dotenv
from openai import OpenAI
import requests
load_dotenv()
import time

# váltotók
state = os.getenv('STATE')
api_key = os.getenv('API_KEY')

# utilsok
def update_env_file(key, value, filename=".env"):
    with open(filename, 'r') as file:
        lines = file.readlines()
    with open(filename, 'w') as file:
        for line in lines:
            if line.startswith(key):
                file.write(f"{key}={value}\n")
            else:
                file.write(line)
def download_image(image_url, save_path):
    # Cseréljük le a szóközöket aláhúzókra
    save_path = save_path.replace(" ", "_") \
                         .replace(".", "") \
                         .replace("'", "") \
                         .replace('"', "")
    
    try:
        response = requests.get(image_url)
        response.raise_for_status()  # Ellenőrzi, hogy a kérés sikeres volt (200-as státusz kód)

        # Kép mentése a megadott útvonalra
        with open(save_path + ".jpg", 'wb') as file:
            file.write(response.content)

        print(f"Kép sikeresen letöltve: {save_path}.jpg")

    except requests.exceptions.RequestException as e:
        print(f"Hiba történt a kép letöltése közben: {e}")

# setup-ok
def setup_ai_text():
    print("--------------- Aphonia AI Setup | AI SET ---------------")
    print("Válassz szöveg motort!")
    print("- [1] GPT-4o")
    print("- [2] GPT-4")
    key_input = input("> ")

    if key_input == "1":
        print("Beállítva: gpt-4o")
        update_env_file('AI_MOTOR', 'gpt-4o')
        setup_ai_image_generation()
    elif key_input == "2":
        print("Beállítva: gpt-4")
        update_env_file('AI_MOTOR', 'gpt-4')
        setup_ai_image_generation()
    else:
        print("[!] Érvénytelen választás!")
        setup_ai_text()
def setup_ai_image_generation():
    print("--------------- Aphonia AI Setup | AI IMAGE GENERATION ---------------")
    print("- [1] DALL-E 3")
    print("- [2] DALL-E 2")
    key_input = input("> ")

    if key_input == "1":
        print("Beállítva: dall-e-3")
        update_env_file('IMAGE_MOTOR', 'dall-e-3')
        update_env_file('STATE','configured')
        os.environ['STATE'] = 'configured'
        print("Most índísd el újra a programot. 5 másodperc mulva kilépés.")
        time.sleep(5)
        exit()
    elif key_input == "2":
        print("Beállítva: dall-e-2")
        update_env_file('IMAGE_MOTOR', 'dall-e-2')
        update_env_file('STATE','configured')
        os.environ['STATE'] = 'configured'
        print("Most índísd el újra a programot. 5 másodperc mulva kilépés.")
        time.sleep(5)
        exit()
    else:
        print("[!] Érvénytelen választás!")
        setup_ai_image_generation()
def setup_api():
    print("--------------- Aphonia AI Setup | API KEY ---------------")
    print("Adj meg egy OpenAI KULCSOT:")
    key_input = input("> ")
    if key_input == "":
        setup_api()

    elif key_input == "exit":
        print("[!] Biztosan ki akkarsz lépni? [I/N]")
        quit_resp = input("> ")
        if quit_resp == "i":
            exit()
        else:
            setup_api()

    else:
        if "sk-" in key_input:
            update_env_file('API_KEY', key_input)
            print("[!] Elfogadva!")
            setup_ai_text()

        else:
            print("")
            print("[!] Nem megfelelő OpenAI API kulcs adj meg újat")
            print("")
            setup_api()

# AI-ok image, text
def ai(user_input):
    api_key = os.getenv('API_KEY')
    model = os.getenv('AI_MOTOR')

    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model=model,
        messages=[
        {"role": "system", "content": "Te vagy Aphonia AI. Segítőkész vagy. És használsz emojikat. Te tudsz képet is generálni a img_gn: <ide a prompt> parancsal angolul írd le az kép generálási prompt-okat. És a parancsokat mindig a válaszod le végére és leg aljára írd!!!"},
        {"role": "user", "content": user_input}
        ]
    )  

    message = "Aphonia: " + response.choices[0].message.content

    return message
def image_gen(prompt):
    api_key = os.getenv('API_KEY')
    model = os.getenv('IMAGE_MOTOR')

    client = OpenAI(api_key=api_key)

    response = client.images.generate(
        model=model,
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    image_url = response.data[0].url

    download_image(image_url, prompt)


def controller():
    while True:
        user = input("Te: ")
        if user == "exit":
            print("[!] Biztosan ki akkarsz lépni? [I/N]")
            quit_resp = input("> ")
            if quit_resp == "i":
                exit()
            else:
                return
        elif user == "settings":
            setup_ai_text()
        else:
            #print(ai(user))
            response = ai(user)
            print(response)

        if "img_gn:" in response:
            prompt = response.split("img_gn:")[1].strip()  
            print("...Generálás...")
            image_gen(prompt)
# csekolás
def check():
    state = os.getenv('STATE')
    if state == "configured":
        print("...STARTED...")
        print("# Parancsok: settings - Rendszer beállítása | exit - Kilépés #")
        controller()
    elif state == "not_configured":
        setup_api()
    else:
        print("[!] Érvénytelen konfiguráció... [Újra alkotás]")
        update_env_file('STATE','not_configured')
        os.environ['STATE'] = 'not_configured'
        check()

check()