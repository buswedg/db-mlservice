# DB ML Service

### Overview:

This Django app provides various API endpoints for users to deploy and manage ML models.

### Dependencies:

Install Docker and Docker Compose:
   - Docker version 26.0.0+ and Docker Compose version 2.28.0+ are required.
   - For Ubuntu, refer to the following link: [https://docs.docker.com/engine/install/ubuntu/](https://docs.docker.com/engine/install/ubuntu/).
   - If you're using Debian or Ubuntu, you can use the bash scripts in the `/helpers` directory to install Docker and Docker Compose:
     ```bash
     bash helpers/install_docker.sh
     bash helpers/install_docker_compose.sh
     ```

### Configuration:

1. Create Configuration Files:
   - Create the following files in the root directory:
     - `dev.env`
     - `prod.env`
     - `superusers.json`
   - Use the respective `*.dist` files as templates for these new files.

2. Generate Django Secret Key:
   - Visit [https://djecrety.ir/](https://djecrety.ir/) or any other suitable tool.
   - Generate a new Django secret key.

3. Set Django Secret Key:
   - Open `dev.env` and `prod.env` files.
   - Set the value of `DJANGO_SECRET_KEY` to the newly obtained secret key.

4. Set Admin Email and Site Name:
   - Open `dev.env` and `prod.env` files.
   - Set the value of `DJANGO_SITE_NAME` to the desired site name.
   - Set the value of `DJANGO_SITE_DOMAIN` to the desired site domain.
   - Set the value of `ADMIN_EMAIL` to the desired admin email address.

5. Set Allowed Hosts (for production environment):
   - Open the `prod.env` file.
   - Set the value of `DJANGO_ALLOWED_HOSTS` to the desired host address(es).
     - Example: `DJANGO_ALLOWED_HOSTS=example.com,www.example.com`

6. Set Database Password:
   - Open the `prod.env` file.
   - Set the value of `DB_PASSWORD` to the desired database password.

7. Set New Admin Account Credentials:
   - Open the `superusers.json` file.
   - Set a new email and password for the admin account in the JSON format.

8. Encrypt/ decrypt *.env/ superusers.json files (optional):
	```bash
	bash helpers/gpg_wrapper.sh -f *.env -e encrypt
	bash helpers/gpg_wrapper.sh -f *.env.gpg -e decrypt
	```

9. Update the included django utilities (optional):
	```bash
	git fetch https://github.com/buswedg/django-utils.git main
	git subtree pull --prefix=apps/utils https://github.com/buswedg/django-utils.git main --squash
	```

10. Update the included playgrounds (optional):
	```bash
	git fetch https://github.com/buswedg/income_classifier.git main
	git subtree pull --prefix=playground/income_classifier https://github.com/buswedg/income_classifier.git main --squash
	```

### Run:

- Run locally for development:
	```bash
	docker compose -f docker-compose.dev.yml --env-file dev.env up
	```

- Run for production (without ssl):
	```bash
	docker compose -f docker-compose.prod.yml --env-file prod.env up
	```

- Run for production (with ssl):
	```bash
	docker compose -f docker-compose.prod.nginx.yml --env-file prod.env up
	```

To inspect emails sent by the app, browse to http://127.0.0.1:8025/

### Connect and use the API:

Grab access and refresh tokens:

```python
import requests

url = "http://127.0.0.1:8000/api/token/"
data = {
  "username": "buswedg", 
  "password": "$PASS"
}

response = requests.post(url, data=data)
data = response.json()

access_token = data.get('access')
refresh_token = data.get('refresh')

headers = {'Authorization': f'JWT {access_token}'}
```

Check endpoints:

```python
url = "http://127.0.0.1:8000/api/v1/endpoints/"
response = requests.get(url, headers=headers)
data = response.json()

print(data)
[{'id': 1,
  'name': 'income_classifier',
  'owner': 'buswedg',
  'created_at': '2023-06-08T23:58:53.287663Z'}]
```

Check ml algorithms:

```python
url = "http://127.0.0.1:8000/api/v1/ml-algorithm/"
response = requests.get(url, headers=headers)
data = response.json()

print(data)
[{'id': 1,
  'name': 'random forest',
  'description': 'Random Forest with simple pre- and post-processing.',
  'code': "class RFClassifier(Helpers):\n    def __init__(self):\n        self.values_fill_missing = joblib.load(os.path.join(ARTIFACTS_PATH, 'train_mode.joblib'))\n        self.encoders = joblib.load(os.path.join(ARTIFACTS_PATH, 'encoders.joblib'))\n        self.model = joblib.load(os.path.join(ARTIFACTS_PATH, 'rf_classifier.joblib'))\n",
  'version': '0.1',
  'owner': 'buswedg',
  'created_at': '2023-06-08T23:58:53.304885Z',
  'parent_endpoint': 1,
  'current_status': 'production'},
 {'id': 2,
  'name': 'extra trees',
  'description': 'Extra Trees with simple pre- and post-processing.',
  'code': "class ETClassifier(Helpers):\n    def __init__(self):\n        self.values_fill_missing = joblib.load(os.path.join(ARTIFACTS_PATH, 'train_mode.joblib'))\n        self.encoders = joblib.load(os.path.join(ARTIFACTS_PATH, 'encoders.joblib'))\n        self.model = joblib.load(os.path.join(ARTIFACTS_PATH, 'et_classifier.joblib'))\n",
  'version': '0.1',
  'owner': 'buswedg',
  'created_at': '2023-06-08T23:58:54.187111Z',
  'parent_endpoint': 1,
  'current_status': 'testing'}]
```

Check ml algorithm status:

```python
url = "http://127.0.0.1:8000/api/v1/ml-algorithm-status/"
response = requests.get(url, headers=headers)
data = response.json()

print(data)
[{'id': 1,
  'active': True,
  'status': 'production',
  'created_by': 'buswedg',
  'created_at': '2023-06-08T23:58:53.309248Z',
  'parent_mlalgorithm': 1},
 {'id': 2,
  'active': True,
  'status': 'testing',
  'created_by': 'buswedg',
  'created_at': '2023-06-08T23:58:54.190485Z',
  'parent_mlalgorithm': 2}]
```

Generate a prediction using a ml algorithm:

```python
url = "http://127.0.0.1:8000/api/v1/predict/income_classifier/?status=production&version=0.1"

payload = {
  "age": 37,
  "workclass": "Private",
  "fnlwgt": 34146,
  "education": "HS-grad",
  "education-num": 9,
  "marital-status": "Married-civ-spouse",
  "occupation": "Craft-repair",
  "relationship": "Husband",
  "race": "White",
  "sex": "Male",
  "capital-gain": 0,
  "capital-loss": 0,
  "hours-per-week": 68,
  "native-country": "United-States"
}

response = requests.post(url, headers=headers, json=payload)
data = response.json()

print(data)
{'probability': 0.07, 
 'label': '<=50K', 
 'status': 'OK', 
 'request_id': 1}
```