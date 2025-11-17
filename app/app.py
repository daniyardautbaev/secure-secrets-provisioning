# app/app.py

import os
import json
import yaml
import hvac
from dotenv import load_dotenv

# -----------------------------
# Load .env variables
# -----------------------------
load_dotenv()  # загружает переменные из .env

env_vars = {
    'api_key': os.environ.get('ENV_API_KEY')  # соответствует твоему .env
}
print("=== ENV VARIABLES ===")
print(env_vars)

# -----------------------------
# Read Config file
# -----------------------------
config_path = os.path.join(os.path.dirname(__file__), 'config.json')
config = None
try:
    with open(config_path, 'r') as f:
        config = json.load(f)
except FileNotFoundError:
    pass

print("\n=== CONFIG FILE ===")
print(config)

# -----------------------------
# Read SOPS encrypted secrets
# -----------------------------
sops_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'secrets', 'secrets.enc.yaml')
sops_secrets = None
try:
    import subprocess
    result = subprocess.run(
        ["sops", "--decrypt", sops_path],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        sops_secrets = yaml.safe_load(result.stdout)
except Exception:
    pass

print("\n=== SOPS SECRETS ===")
print(sops_secrets)

# -----------------------------
# Read Vault KV v2 secrets
# -----------------------------
def read_from_vault():
    vault_addr = os.environ.get("VAULT_ADDR", "http://127.0.0.1:8200")
    vault_token = os.environ.get("VAULT_TOKEN")
    print("\nUsing Vault Token:", vault_token)

    client = hvac.Client(url=vault_addr, token=vault_token)

    if not client.is_authenticated():
        raise Exception("Vault authentication failed! Check VAULT_TOKEN.")

    # Чтение секрета из KV v2
    secret = client.secrets.kv.v2.read_secret_version(
        path="myapp",
        mount_point="secret",  # важно указать mount_point
    )
    return secret['data']['data']

vault_secrets = None
try:
    vault_secrets = read_from_vault()
except Exception as e:
    print("\n=== VAULT SECRETS ===")
    print("Error reading Vault secrets:", e)
else:
    print("\n=== VAULT SECRETS ===")
    print(vault_secrets)

# -----------------------------
# Main
# -----------------------------
def main():
    print("\n--- SUMMARY ---")
    print("ENV:", env_vars)
    print("Config:", config)
    print("SOPS:", sops_secrets)
    print("Vault:", vault_secrets)

if __name__ == "__main__":
    main()
