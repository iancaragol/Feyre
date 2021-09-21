# This script creates a GitHub secret
from base64 import b64encode

from nacl import encoding, public
import argparse
import os
import requests
import json

dirname = os.path.abspath(os.path.dirname(__file__))

# Instantiate the parser
parser = argparse.ArgumentParser(description='Create a secret via the GitHub API')
parser.add_argument("--secret-key", help="the name of the secret to encrypt", type=str, required=True)
parser.add_argument("--secret-value", help="the secret value to encrypt", type=str, required=True)
args = parser.parse_args()

# Get the repo secret secretsss
with open(f'{dirname}/repo_secret.json', 'r') as f:
    data = json.loads(f.read())
    pat = data['pat']
    public_key_id = data['public_key_id']
    public_key = data['public_key']

def encrypt(public_key: str, secret_value: str) -> str:
    """
    Encrypt a Unicode string using the public key.
    """

    public_key = public.PublicKey(public_key.encode("utf-8"), encoding.Base64Encoder())
    sealed_box = public.SealedBox(public_key)
    encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
    return b64encode(encrypted).decode("utf-8")

def post_secret(secret_key: str, secret_value: str) -> None:
    """
    Post a secret to the GitHub API.
    """

    url = f"https://api.github.com/repos/iancaragol/Feyre/actions/secrets/{secret_key}"
    headers = {
        "Authorization": "Bearer {}".format(pat),
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json"
    }
    data = {
        "encrypted_value": encrypt(public_key, secret_value),
        "key_id": public_key_id
    }
    response = requests.put(url, headers=headers, json=data)
    response.raise_for_status()

    if response.status_code == 201:
        print("Secret created successfully!")
        return
    else:
        print("Something went wrong")
        print(response.status_code)
        print(response.text)

if __name__ == "__main__":
    post_secret(args.secret_key, args.secret_value)
