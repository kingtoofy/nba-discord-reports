import requests

def send(webhook, message):
    payload = {"content": message}
    requests.post(webhook, json=payload)
