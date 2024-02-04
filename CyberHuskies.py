#CyberHuskies




#Link to website for scannign documents
#https://gretel.ai/blog/automate-detecting-sensitive-personally-identifiable-information-pii-with-gretel
#https://www.makeuseof.com/python-create-document-scanner/






from gretel_client import get_cloud_client


# Connect to Gretel with your API key


client = get_cloud_client(prefix="api", api_key="grtuc5c8f1506ce274fa026d375c0c63d7bf1ac9290d6f247b09160459dffd8916d5")
client.install_packages()
