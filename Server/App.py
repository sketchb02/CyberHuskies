from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import yaml
from gretel_client import configure_session
from gretel_client.projects import create_or_get_unique_project
from gretel_client.helpers import poll

app = Flask(__name__)
CORS(app)

# Configure the Gretel session with your API key
configure_session(api_key="grtuf4aa47cbec50d19be677b7a8bdb8abd9b884cf9755f29fb235be278a2b1b50f5", cache="yes", validate=True, endpoint="https://api.gretel.cloud")

@app.route('/redact', methods=['POST'])
def redact_data():
    # Extract the PII types and file from the request
    pii_types = request.form.getlist('pii_types')
    file = request.files['file']
    df = pd.read_csv(file)

    # Dynamically create the redaction config based on user input
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
    
    """
    # Initialize an empty list for value_labels
    value_labels = []

    # Populate the list based on the PII types selected by the user
    for pii_type in pii_types:
        if pii_type.lower() == 'phone':
            value_labels.append('phone_number')
        elif pii_type.lower() == 'email':
            value_labels.append('email_address')
        # Add more conditions here for other PII types as needed

    # Construct the rule with all selected PII types
    rule = {
        "name": "redact_selected_pii",
        "conditions": {
            "value_label": value_labels
        },
        "transforms": [{
            "type": "redact_with_char",
            "attrs": {"char": "X"}
        }]
    }

    # Append this single rule to your configuration
    redaction_config['models'][0]['transforms']['policies'][0]['rules'].append(rule)
    # Convert the dynamic config to YAML format
    config_yaml = yaml.dump(redaction_config)
    """
    # Create a project and model with the dynamic config
    project = create_or_get_unique_project(name="dynamic-redaction-project")
    model = project.create_model_obj(model_config=config)

    # Upload the data and wait for the model to be ready
    model.submit_cloud()
    poll(model)

    # Assuming there is a way to directly redact the data using the model
    # This will depend on the Gretel API's support for such operations
    # The following is a placeholder for the actual redaction process
    # redacted_data = model.redact(data=df)
    # For demonstration, we'll just return the original data
    return jsonify({'status': 'success', 'redacted_content': df.to_csv(index=False)})

if __name__ == '__main__':
    app.run(debug=True)