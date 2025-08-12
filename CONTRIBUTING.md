# Contributing to Reshop

Спасибо за интерес к проекту Reshop! Мы приветствуем вклад от сообщества.

## 🚀 Как начать

### 1. Форк и клонирование

1. Форкните репозиторий на GitHub
2. Клонируйте ваш форк локально:
   ```bash
   git clone https://github.com/rel0ker/reshop.git
   cd reshop
   ```

### 2. Настройка окружения

#### Backend (Django)
```bash
# Создание виртуального окружения
python -m venv venv

# Активация
source venv/bin/activate  # Linux/macOS
# или
venv\Scripts\activate     # Windows

# Установка зависимостей
pip install -r requirements.txt
pip install -r requirements-dev.txt  # для разработки

# Настройка переменных окружения
cp env.example .env
# Отредактируйте .env файл

# Миграции
python manage.py migrate

# Создание суперпользователя
python manage.py createsuperuser
```

#### Frontend (Vue.js)
```bash
cd frontend-vue

# Установка зависимостей
npm install

# Запуск в режиме разработки
npm run dev
```

## 🔧 Разработка

### Структура проекта

- `core/` - Django приложение с основным функционалом
- `digital_marketplace/` - настройки Django проекта
- `frontend-vue/` - Vue.js фронтенд
- `docs/` - документация

### Стиль кода

#### Python (Backend)
- Следуйте PEP 8
- Используйте Black для форматирования
- Добавляйте типы с помощью type hints
- Покрывайте код тестами

```bash
# Форматирование
black .
isort .

# Линтинг
flake8 .

# Тесты
python manage.py test
pytest
```

#### JavaScript/TypeScript (Frontend)
- Следуйте ESLint правилам
- Используйте Prettier для форматирования
- Добавляйте типы TypeScript

```bash
# Форматирование
npm run format

# Линтинг
npm run lint

# Тесты
npm test
```

### Создание новой функции

1. Создайте новую ветку:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Внесите изменения

3. Добавьте тесты

4. Зафиксируйте изменения:
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

5. Отправьте изменения:
   ```bash
   git push origin feature/your-feature-name
   ```

6. Создайте Pull Request

## 📝 Commit Convention

Используйте [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` - новая функция
- `fix:` - исправление бага
- `docs:` - изменения в документации
- `style:` - форматирование, отсутствующие точки с запятой и т.д.
- `refactor:` - рефакторинг кода
- `test:` - добавление тестов
- `chore:` - обновление задач сборки, настройки и т.д.

## 🧪 Тестирование

### Backend тесты
```bash
# Все тесты
python manage.py test

# Конкретное приложение
python manage.py test core

# С покрытием
coverage run --source='.' manage.py test
coverage report
coverage html
```

### Frontend тесты
```bash
# Unit тесты
npm run test:unit

# E2E тесты
npm run test:e2e

# Покрытие
npm run test:coverage
```

## 🐛 Отчеты об ошибках

При создании Issue:

1. Опишите проблему четко и кратко
2. Укажите шаги для воспроизведения
3. Опишите ожидаемое и фактическое поведение
4. Укажите версии:
   - Python
   - Django
   - Node.js
   - Vue.js
   - Операционная система

## 💡 Предложения функций

1. Проверьте существующие Issues
2. Создайте Issue с описанием функции
3. Обсудите с командой
4. Создайте Pull Request после одобрения

## 🔒 Безопасность

Если вы нашли уязвимость безопасности:

1. **НЕ** создавайте публичный Issue
2. Отправьте email на security@your-domain.com
3. Опишите уязвимость подробно
4. Мы ответим в течение 48 часов

## 📚 Документация

- Обновляйте README.md при изменении API
- Добавляйте комментарии к сложному коду
- Создавайте документацию для новых функций

## 🤝 Code Review

Все Pull Request'ы проходят review:

1. Проверьте CI/CD статус
2. Убедитесь, что тесты проходят
3. Обновите документацию при необходимости
4. Отвечайте на комментарии reviewer'а

## 📄 Лицензия

Внося изменения, вы соглашаетесь с тем, что ваш вклад будет лицензирован под MIT License.

## 🆘 Нужна помощь?

- Создайте Issue с вопросом
- Присоединитесь к нашему Discord/Telegram
- Обратитесь к документации

Спасибо за ваш вклад! 🎉
