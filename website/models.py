import speech_recognition as sr
import pyttsx3
import time
import qrcode
import cv2
from pyzbar.pyzbar import decode
from bs4 import BeautifulSoup
import requests
from web3 import Web3

def smart_contract(p_key,send_add,rec_add,amount):
    # Replace with your Ethereum node URL
    web3 = Web3(Web3.HTTPProvider('https://rpc-mumbai.maticvigil.com'))

    # Replace with the deployed contract address
    contract_address = '0xd9145CCE52D386f254917e481eB44e9943F39138'

    # Replace with the ABI of your contract
    contract_abi = [
        {
            "inputs": [
                {
                    "internalType": "address payable",
                    "name": "_to",
                    "type": "address"
                },
                {
                    "internalType": "uint256",
                    "name": "_amount",
                    "type": "uint256"
                }
            ],
            "name": "sendEther",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "inputs": [],
            "stateMutability": "nonpayable",
            "type": "constructor"
        },
        {
            "stateMutability": "payable",
            "type": "receive"
        },
        {
            "inputs": [],
            "name": "getBalance",
            "outputs": [
                {
                    "internalType": "uint256",
                    "name": "",
                    "type": "uint256"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [],
            "name": "owner",
            "outputs": [
                {
                    "internalType": "address",
                    "name": "",
                    "type": "address"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        }
    ]  # Replace this with your actual ABI

    # Replace with your private key
    private_key = p_key

    # Set the gas price and gas limit
    gas_price = web3.to_wei('50', 'gwei')
    gas_limit = 3000000

    # Set the sender and receiver addresses
    sender_address = send_add
    receiver_address = Web3.to_checksum_address(rec_add)

    # Set up the contract instance
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)

    # Calculate the amount to send in Wei
    amount_to_send = web3.to_wei(amount, 'gwei')

    # Call the sendEther function on the contract with the required arguments
    transaction = contract.functions.sendEther(receiver_address, amount_to_send).build_transaction({
        'gas': gas_limit,
        'gasPrice': gas_price,
        'from': sender_address,
        'nonce': web3.eth.get_transaction_count(sender_address),
    })

    # Sign the transaction
    signed_transaction = web3.eth.account.sign_transaction(transaction, private_key)

    # Send the signed transaction
    transaction_hash = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)

    # Wait for the transaction to be mined
    receipt = web3.eth.wait_for_transaction_receipt(transaction_hash)

    print(f"Ether sent successfully. Transaction hash: {transaction_hash}")

def voice(user_p_key,user_add):
    # instantiating the Recognizer and Microphone classes
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    terminate = False
    while not terminate:
        try:
            # Setting up the text-to-speech engine
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            engine.setProperty('voice', voices[1].id)
            engine.setProperty('rate', 150)
            engine.setProperty('volume', 1.0)

            with mic as source:
                engine.say('Listening')
                engine.runAndWait()
                print("Listening...")

                # Converting speech-to-text
                recognizer.adjust_for_ambient_noise(source, duration=0.2)
                recognizer.dynamic_energy_threshold = True
                audio = recognizer.listen(source, 3, 10)
                audioText = recognizer.recognize_google(audio)
                print(audioText)
                audioText = audioText.lower()

                if audioText == "receive money":
                    engine.say("Before we start kindly provide your wallet address")
                    engine.runAndWait()
                    img = qrcode.make(user_add)
                    type(img)
                    img.save("qr_build.png")

                if audioText == "send money":
                    amount = input("Enter the amount you want to transfer in gwei")
                    cap = cv2.VideoCapture(0)
                    abc = 0

                    while True:
                        # Capture frame-by-frame
                        ret, frame = cap.read()

                        # Decode QR code
                        d = decode(frame)
                        for barcode in d:
                            bar = barcode.data.decode()
                            abc = 1

                        # Display the resulting frame
                        cv2.imshow('QR Code Scanner', frame)

                        # Break the loop on 'q' key press
                        if cv2.waitKey(1) & 0xFF == ord('q') or abc == 1:
                            break

                    # When everything done, release the capture
                    cap.release()
                    cv2.destroyAllWindows()

                    smart_contract(user_p_key, user_add, bar, amount)

                if audioText == 'get balance':
                    web3 = Web3(Web3.HTTPProvider('https://rpc-mumbai.maticvigil.com'))

                    # Replace with the deployed contract address
                    contract_address = '0xd9145CCE52D386f254917e481eB44e9943F39138'
                    balance = web3.eth.get_balance(user_add)
                    print(balance)

                if audioText == "give me my net worth":
                    url = f'https://www.google.com/search?q=ethereum+value+today'

                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
                    }
                    response = requests.get(url, headers=headers)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    price_element = soup.find("div", class_="BNeawe iBp4i AP7Wnd")
                    if price_element:
                        price = price_element.text
                        new = ""
                        for i in price:
                            if i == ',':
                                continue
                            new = new + i
                            if i == " ":
                                break
                    web3 = Web3(Web3.HTTPProvider('https://rpc-mumbai.maticvigil.com'))

                    # Replace with the deployed contract address
                    contract_address = '0xd9145CCE52D386f254917e481eB44e9943F39138'
                    balance = web3.eth.get_balance(user_add)

                    real_money = (float(balance) / 10 ** 18) * float(new)
                    print(real_money)

                if audioText == 'exit' or 'quit':
                    break

        except sr.UnknownValueError:
            output = "Unable to recognize speech"
            print(output)
            engine.say(output)
            time.sleep(0.5)
            engine.say("retry")
            engine.runAndWait()
            terminate = False

        except sr.WaitTimeoutError:
            output = "You took too long"
            print(output)
            engine.say(output)
            time.sleep(0.5)
            engine.say("retry")
            engine.runAndWait()
            terminate = False