#!/usr/bin/env python3
"""
Скрипт для проверки готовности проекта к продакшену
"""

import os
import sys
from pathlib import Path

def check_file_exists(file_path, description):
    """Проверяет существование файла"""
    if os.path.exists(file_path):
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ {description}: {file_path} - НЕ НАЙДЕН")
        return False

def check_environment_variables():
    """Проверяет переменные окружения"""
    print("\n🔍 Проверка переменных окружения...")
    
    required_vars = [
        'SECRET_KEY',
        'POSTGRES_PASSWORD',
        'ALLOWED_HOSTS',
        'YOOKASSA_SHOP_ID',
        'YOOKASSA_SECRET_KEY'
    ]
    
    env_file = 'env.production'
    if not os.path.exists(env_file):
        print(f"❌ Файл {env_file} не найден")
        return False
    
    with open(env_file, 'r') as f:
        content = f.read()
    
    missing_vars = []
    for var in required_vars:
        if var in content and not content.split(var + '=')[1].split('\n')[0].startswith('your_'):
            print(f"✅ {var}: настроен")
        else:
            print(f"❌ {var}: не настроен или использует значение по умолчанию")
            missing_vars.append(var)
    
    return len(missing_vars) == 0

def check_security_settings():
    """Проверяет настройки безопасности"""
    print("\n🛡️ Проверка настроек безопасности...")
    
    # Проверяем Django settings
    settings_file = 'digital_marketplace/settings_production.py'
    if os.path.exists(settings_file):
        with open(settings_file, 'r') as f:
            content = f.read()
        
        security_checks = [
            ('DEBUG = False', 'DEBUG отключен'),
            ('SECURE_SSL_REDIRECT', 'SSL редирект настроен'),
            ('SECURE_HSTS_SECONDS', 'HSTS настроен'),
            ('X_FRAME_OPTIONS', 'X-Frame-Options настроен')
        ]
        
        for check, description in security_checks:
            if check in content:
                print(f"✅ {description}")
            else:
                print(f"❌ {description} - не настроен")
    else:
        print(f"❌ Файл {settings_file} не найден")

def check_docker_files():
    """Проверяет Docker файлы"""
    print("\n🐳 Проверка Docker файлов...")
    
    docker_files = [
        ('Dockerfile.production', 'Production Dockerfile'),
        ('docker-compose.production.yml', 'Production docker-compose'),
        ('nginx.production.conf', 'Production nginx конфигурация')
    ]
    
    all_exist = True
    for file_path, description in docker_files:
        if check_file_exists(file_path, description):
            all_exist = all_exist and True
        else:
            all_exist = False
    
    return all_exist

def check_frontend_production():
    """Проверяет готовность фронтенда к продакшену"""
    print("\n🎨 Проверка готовности фронтенда...")
    
    frontend_files = [
        ('frontend-vue/vite.config.production.ts', 'Production Vite конфигурация'),
        ('frontend-vue/Dockerfile.production', 'Production Dockerfile'),
        ('frontend-vue/nginx.conf', 'Nginx конфигурация')
    ]
    
    all_exist = True
    for file_path, description in frontend_files:
        if check_file_exists(file_path, description):
            all_exist = all_exist and True
        else:
            all_exist = False
    
    return all_exist

def check_ssl_certificates():
    """Проверяет SSL сертификаты"""
    print("\n🔒 Проверка SSL сертификатов...")
    
    ssl_dir = 'ssl'
    if os.path.exists(ssl_dir):
        cert_files = ['cert.pem', 'key.pem']
        for cert_file in cert_files:
            cert_path = os.path.join(ssl_dir, cert_file)
            if os.path.exists(cert_path):
                print(f"✅ SSL сертификат: {cert_path}")
            else:
                print(f"❌ SSL сертификат: {cert_path} - не найден")
    else:
        print(f"⚠️  Папка {ssl_dir} не найдена. Создайте её и поместите SSL сертификаты")

def main():
    """Основная функция проверки"""
    print("🚀 Проверка готовности проекта к продакшену")
    print("=" * 60)
    
    checks_passed = 0
    total_checks = 6
    
    # Проверка файлов
    if check_file_exists('env.production', 'Файл переменных окружения'):
        checks_passed += 1
    
    if check_environment_variables():
        checks_passed += 1
    
    check_security_settings()
    checks_passed += 1
    
    if check_docker_files():
        checks_passed += 1
    
    if check_frontend_production():
        checks_passed += 1
    
    check_ssl_certificates()
    checks_passed += 1
    
    # Итоговая оценка
    print("\n" + "=" * 60)
    print(f"📊 Результат проверки: {checks_passed}/{total_checks}")
    
    if checks_passed == total_checks:
        print("🎉 Проект готов к продакшену!")
        print("\n📋 Следующие шаги:")
        print("1. Настройте SSL сертификаты")
        print("2. Запустите: make deploy")
        print("3. Проверьте: make health-check")
    else:
        print("⚠️  Проект НЕ готов к продакшену!")
        print("\n🔧 Что нужно исправить:")
        print("- Проверьте все ❌ ошибки выше")
        print("- Настройте недостающие файлы")
        print("- Запустите проверку снова")
    
    return checks_passed == total_checks

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
