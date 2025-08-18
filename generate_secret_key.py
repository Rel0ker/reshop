#!/usr/bin/env python3
"""
Скрипт для генерации безопасного секретного ключа Django
"""

import secrets
import string

def generate_secret_key(length=50):
    """Генерирует безопасный секретный ключ"""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def generate_django_secret_key():
    """Генерирует секретный ключ в формате Django"""
    return ''.join(secrets.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(50))

if __name__ == "__main__":
    print("🔐 Генерация секретного ключа для Django")
    print("=" * 50)
    
    # Генерируем несколько вариантов
    for i in range(3):
        secret_key = generate_django_secret_key()
        print(f"Вариант {i+1}: {secret_key}")
        print()
    
    print("⚠️  ВАЖНО:")
    print("1. Выберите один из ключей выше")
    print("2. Поместите его в переменную SECRET_KEY в env.production")
    print("3. Никогда не коммитьте секретный ключ в git!")
    print("4. Храните ключ в безопасном месте")
    print()
    print("🔒 Рекомендуется использовать менеджер секретов (например, HashiCorp Vault)")
