import argparse
import requests

parser = argparse.ArgumentParser()
parser.add_argument('-e', '--email', action='store', required=True, help="User's email who can create new user")
parser.add_argument('-p', '--password', action='store', required=True, help='Password user')
args = parser.parse_args()

print("================================= Users tests creation ==================================")

body_manager = {'email': 'manager@pytest.com',
                'password': 'test01234',
                'first_name': 'Joslin',
                'last_name': 'Martimou',
                'role': 'Manager'}

body_salesperson = {'email': 'salesperson@pytest.com',
                    'password': 'test01234',
                    'first_name': 'André',
                    'last_name': 'Pizouli',
                    'role': 'Salesperson'}

body_techincal_support = {'email': 'technical_support@pytest.com',
                          'password': 'test01234',
                          'first_name': 'Camille',
                          'last_name': 'Robichon',
                          'role': 'Technical support'}


# Login
response_login = requests.post("http://localhost:8000/login/",
                               json={"email": args.email, "password": args.password})

token = f"Bearer {response_login.json()['access']}"

# Creation
requests.post("http://localhost:8000/users/", json=body_manager, headers={"Authorization": token})
requests.post("http://localhost:8000/users/", json=body_salesperson, headers={"Authorization": token})
requests.post("http://localhost:8000/users/", json=body_techincal_support, headers={"Authorization": token})

# Check
check_users = {'manager@pytest.com': 'Fail', 'salesperson@pytest.com': 'Fail', 'technical_support@pytest.com': 'Fail'}
response = requests.get("http://localhost:8000/users/", headers={"Authorization": token})

for d in response.json():
    for user in check_users:

        if user in d['email']:
            check_users[user] = 'Success'
            break

for k, v in check_users.items():
    print(f"{k} : {v}")
