import os
import yaml
from dotenv import load_dotenv
import subprocess
import hvac

# Load .env variables
load_dotenv()

def read_env():
    return {
        "api_key": os.getenv("ENV_API_KEY")
    }

def read_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

def read_sops_file():
    result = subprocess.run(
        ["sops", "--decrypt", "secrets.enc.yaml"],
        capture_output=True,
        text=True
    )
    return yaml.safe_load(result.stdout)

def read_from_vault():
    client = hvac.Client(url="http://127.0.0.1:8200", token="root")
    secret = client.secrets.kv.v2.read_secret_version(path="myapp")
    return secret["data"]["data"]

def main():
    print("=== ENV VARIABLES ===")
    print(read_env())

    print("\n=== CONFIG FILE ===")
    print(read_config())

    print("\n=== SOPS SECRETS ===")
    print(read_sops_file())

    print("\n=== VAULT SECRETS ===")
    print(read_from_vault())


if __name__ == "__main__":
    main()

