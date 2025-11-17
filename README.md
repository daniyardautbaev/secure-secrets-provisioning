# Secure Secrets Provisioning

Простой пример безопасного управления секретами в Python-приложении.  
Секреты загружаются из:

- ENV переменных (`.env`)  
- Конфигурационного файла (`config.json`)  
- Зашифрованного SOPS файла (`secrets.enc.yaml`)  
- HashiCorp Vault (KV v2)  


## Установка и запуск

1. Клонируем репозиторий:

```bash
git clone https://github.com/daniyardautbaev/secure-secrets-provisioning.git
cd secure-secrets-provisioning
```
Создаём виртуальное окружение и устанавливаем зависимости:
```

python3 -m venv venv
source venv/bin/activate


pip install -r app/requirements.txt
```
```

ENV_API_KEY=API_KEY
VAULT_ADDR=http://127.0.0.1:8200
VAULT_TOKEN=Token

```
Запуск приложения:
```

python3 app/app.py
```

