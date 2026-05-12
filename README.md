# Спарнюк Владислав Александрович 
# Sparnjk_VA_23
# 3 курс / 6 семестр
# Искусственный интеллект
# Курсовая работа

# Carbon Way - Крипто-кошелек: Аудит углеродного следа

Система динамического аудита углеродного следа крипто-кошельков с классификацией транзакций по типам активности и расчетом стоимости компенсации.

## Архитектура и стек

### Backend
- **FastAPI** (Python 3.10+) - асинхронный веб-фреймворк
- **SQLAlchemy (async)** - ORM для работы с БД
- **PostgreSQL** - основная база данных
- **Redis** - кэширование и хранение статуса задач
- **httpx** - асинхронный HTTP-клиент для запросов к Blockscout API

### Frontend
- **React** (Vite) - фронтенд фреймворк
- **Tailwind CSS** - CSS-фреймворк
- **Recharts** - библиотека для графиков
- **Lucide React** - иконки

## Функционал

1. **Аудит углеродного следа** по транзакциям кошелька
2. **Классификация транзакций** по типам: DeFi, NFT, Transfer
3. **Динамические коэффициенты** эмиссии CO₂ (обновляются каждые 24 часа)
4. **Расчет стоимости компенсации** углеродного следа
5. **Визуализация** (графики, диаграммы)
6. **Экологический паспорт кошелька**
7. **Наглядные аналогии** (часы работы чайника, км на электромобиле и т.д.)

## Установка и запуск

### Предварительные требования
- Python 3.10+
- Node.js 18+
- PostgreSQL (нативная установка)
- Redis (нативная установка)

### 1. Клонирование репозитория
```bash
git clone https://github.com/Ramzik-iou/Kursovaya_Carbon_Way.git
cd Kursovaya_Carbon_Way
```

### 2. Настройка переменных окружения
Скопируйте `.env.example` в `.env` и заполните ваши данные:
```bash
cp .env.example .env
```

Отредактируйте `.env`:
```
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/carbon_way
REDIS_URL=redis://localhost:6379/0
```

### 3. Backend

#### Создание виртуального окружения
```bash
python -m venv .venv
```

#### Активация виртуального окружения
Windows (PowerShell):
```powershell
. .venv\Scripts\Activate.ps1
```

Linux/macOS:
```bash
source .venv/bin/activate
```

#### Установка зависимостей
```bash
pip install -r backend/requirements.txt
```

#### Создание базы данных в PostgreSQL
```sql
CREATE DATABASE carbon_way;
```

#### Запуск backend
```bash
python -m backend.main
```
или
```bash
cd backend
python main.py
```

Backend будет доступен по адресу: `http://localhost:8000`

Документация API (Swagger): `http://localhost:8000/docs`

### 4. Frontend

#### Установка зависимостей
```bash
cd frontend
npm install
```

#### Запуск frontend в режиме разработки
```bash
npm run dev
```

Frontend будет доступен по адресу: `http://localhost:3000`

## Структура проекта

```
Kursovaya_Carbon_Way/
├── backend/                 # Backend на FastAPI
│   ├── calculator.py        # Логика расчета углеродного следа
│   ├── database.py          # Модели БД и инициализация
│   ├── intensity_updater.py # Динамическое обновление коэффициентов
│   ├── main.py              # Основной API файл
│   ├── requirements.txt     # Зависимости Python
│   ├── scanner.py           # Интеграция с Blockscout API
│   └── schemas.py           # Pydantic схемы
├── frontend/                # Frontend на React
│   ├── src/
│   │   ├── components/      # Компоненты (Dashboard, Charts, Analogies)
│   │   ├── App.jsx          # Основной компонент
│   │   └── main.jsx         # Точка входа
│   └── package.json         # Зависимости npm
├── .env.example             # Пример переменных окружения
└── .gitignore               # Файлы для игнорирования в Git
```

## Использование

1. Введите адрес крипто-кошелька в поле ввода
2. Нажмите "Analyze Wallet"
3. Подождите завершения анализа (статус "In Progress")
4. Посмотрите результаты:
   - Общий углеродный след
   - Экономия CO₂ за счет Layer 2
   - Стоимость компенсации
   - Графики распределения по сетям и типам активности
   - Наглядные аналогии
   - Экологический паспорт кошелька

## Поддерживаемые сети

- Ethereum (Mainnet)
- Polygon
- Optimism

## Лицензия

MIT

