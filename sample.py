import requests
email = "awaisahmadkhanlist@gmail.com"
req = requests.get(f"http://18.130.61.93:8080/email-check/{email}")
print(req.json())

