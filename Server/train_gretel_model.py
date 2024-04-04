import os
import pandas as pd
import yaml
from faker import Faker
from gretel_client import configure_session, get_cloud_client
from gretel_client.helpers import poll
from gretel_client.projects import create_or_get_unique_project

# Set the API key for Gretel
configure_session(api_key="grtuf4aa47cbec50d19be677b7a8bdb8abd9b884cf9755f29fb235be278a2b1b50f5grtuc5c8f1506ce274fa026d375c0c63d7bf1ac9290d6f247b09160459dffd8916d5", cache="yes", validate=True, endpoint="https://api.gretel.ai")

# Model configuration with transformations and rules (use your config from earlier)
config = """
schema_version: "1.0"
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
                    char: "X"
label_predictors:
  namespace: custom
  regex:
    user_id:
      patterns:
        - score: high
          regex: "user_[\\d]{5}"
"""

# Use Faker to generate training data
def fake_pii_csv(filename, lines=100):
    fake = Faker()
    with open(filename, "w") as f:
        f.write("id,name,email,phone,visa,ssn,user_id\n")
        for i in range(lines):
            _name = fake.name()
            _email = fake.email()
            _phone = fake.phone_number()
            _cc = fake.credit_card_number(card_type=None)
            _ssn = fake.ssn()
            _id = f'user_{fake.numerify(text="#####")}'
            f.write(f"{i},{_name},{_email},{_phone},{_cc},{_ssn},{_id}\n")

output_folder = './'

# Create training CSV file
fake_pii_csv(os.path.join(output_folder, "train.csv"))

# Create a project and model configuration
client = get_cloud_client()
project = create_or_get_unique_project(name="redact-pii-transform")
model = project.create_model_obj(
    model_config=yaml.safe_load(config), data_source=os.path.join(output_folder, "train.csv")
)

# Upload the training data and train the model
model.submit_cloud()
poll(model)

# Output the model identifiers for later use
print(f"Project Name: {project.name}")
print(f"Model ID: {model.model_id}")
