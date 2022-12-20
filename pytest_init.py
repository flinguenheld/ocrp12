import argparse
import requests

parser = argparse.ArgumentParser()
parser.add_argument('-e', '--email', action='store', required=True, help="User's email who can create new user")
parser.add_argument('-p', '--password', action='store', required=True, help='Password user')
args = parser.parse_args()

print("================================= Users test creation ==================================")

users = {
        'body_manager': [{'email': 'manager@pytest.com',
                          'password': 'test01234',
                          'first_name': 'Joslin',
                          'last_name': 'Martimou',
                          'role': 'Manager'},
                         ''],

        'body_salesperson': [{'email': 'salesperson@pytest.com',
                              'password': 'test01234',
                              'first_name': 'André',
                              'last_name': 'Pizouli',
                              'role': 'Salesperson'},
                             ''],

        'body_salesperson_2': [{'email': 'salesperson_2@pytest.com',
                                'password': 'test01234',
                                'first_name': 'André_2',
                                'last_name': 'Pizouli_2',
                                'role': 'Salesperson'},
                               ''],

        'body_techincal_support': [{'email': 'technical_support@pytest.com',
                                    'password': 'test01234',
                                    'first_name': 'Camille',
                                    'last_name': 'Robichon',
                                    'role': 'Technical support'},
                                   ''],

        'body_test_user': [{'email': 'test@test.com',
                            'password': 'test01234',
                            'first_name': 'Bernald',
                            'last_name': 'Testeur',
                            'role': 'Manager'},
                           '']
        }

# Login
response_login = requests.post("http://localhost:8000/login/",
                               json={"email": args.email, "password": args.password})

token = f"Bearer {response_login.json()['access']}"

# Creation
for user in users.values():
    response = requests.post("http://localhost:8000/users/", json=user[0], headers={"Authorization": token})
    user[1] = f'status code {response.status_code}'

# Check
response = requests.get("http://localhost:8000/users/", headers={"Authorization": token})

for d in response.json():
    for k, v in users.items():

        if v[0]['email'] in d['email']:
            v[1] += ' - User ok in the database'
            break

for k, v in users.items():
    print(f"{k} : {v[1]}")
