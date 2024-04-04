
import os 

# Connect to Gretel with your API key
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
new_url = 'https://gretel.ai'


session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

session.get(new_url)

from gretel_client import Gretel

import pandas as pd
from gretel_client import configure_session
pd.set_option("max_colwidth", None)
configure_session(api_key="grtua3b99d6cf0837c952ea39c43ec9558f3fcd45230bc9962814af16f7e64e9b627", cache="yes", validate=True, endpoint="https://api.gretel.ai")

#  Configuration with transformations and rules

config = """schema_version: "1.0"
name: "Redact PII"
models:
  - transforms:
      data_source: "_"
      policies:
        - name: remove_pii
          rules:
            - name: redact_ssn_and_user_id
              conditions:
                value_label:
                  - us_social_security_number
                  - custom/user_id
                  - visa
                  - phone_number
                  - email_address
              transforms:
                - type: redact_with_char
                  attrs:
                    char: X
label_predictors:
  namespace: custom
  regex:
    user_id:
      patterns:
        - score: high
          regex: 'user_[\d]{5}'
"""

from faker import Faker

# Use Faker to make training and test data.
def fake_pii_csv(filename, lines=100):
    fake = Faker()
    with open(filename, "w") as f:
        f.write("id,name,email,phone,visa,ssn,user_id\n")
        for i in range(lines):
            _name = fake.name()
            _email = fake.email()
            _phone = fake.phone_number()
            _cc = fake.credit_card_number()
            _ssn = fake.ssn()
            _id = f'user_{fake.numerify(text="#####")}'
            f.write(f"{i},{_name},{_email},{_phone},{_cc},{_ssn},{_id}\n")

output_folder = os.path.dirname(os.path.abspath(__file__))

fake_pii_csv(os.path.join(output_folder, "train.csv"))
fake_pii_csv(os.path.join(output_folder,"test.csv"))
 
import yaml

from gretel_client.projects import create_or_get_unique_project
from gretel_client.helpers import poll

# Create a project and model configuration.
project = create_or_get_unique_project(name="redact-pii-transform")

model = project.create_model_obj(
    model_config=yaml.safe_load(config), data_source=os.path.join(output_folder, "train.csv")
)




# Upload the training data.  Train the model.
model.submit_cloud()

poll(model)

# Use the model to generate synthetic data.
record_handler = model.create_record_handler_obj(data_source=os.path.join(output_folder, "test.csv"))

record_handler.submit_cloud()

poll(record_handler)

#  Here is our "before."
train_df = pd.read_csv(os.path.join(output_folder, "test.csv"))
print("test.csv head, before redaction")
print(train_df.head())

# And here is our "after."
transformed = pd.read_csv(record_handler.get_artifact_link("data"), compression="gzip")
print("test.csv head, after redaction")
transformed.head()
