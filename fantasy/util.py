import requests

def send_to_discord(message, webhook_url):
    payload = {
        "content": message  # This is the message you want to send
    }
    headers = {
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(webhook_url, json=payload, headers=headers)
        if response.status_code == 204:
            print("Message sent to Discord successfully!")
        else:
            print(f"Failed to send message. Status code: {response.status_code}")
    except:
        print(f"Failed to send message.")
        pass
    
  
