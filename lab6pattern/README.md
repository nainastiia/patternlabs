# Smart Day Planner: Планувальник на Основі Погодних Умов

Цей проект реалізує веб-сервіс Smart Day Planner, який пропонує щоденний план активностей на основі погодних умов, використовуючи дизайн-патерни **Strategy** та **Observer**.

## Дизайн-Патерни

1.  **Strategy (Стратегія):** Використовується для визначення алгоритму планування на основі поточної **погоди**. Кожна погодна умова (`Sunny`, `Rainy`, `Snowy`, `Cloudy`) має свою конкретну стратегію, яка пропонує оптимальний набір активностей.
2.  **Observer (Спостерігач):** **WeatherStation** (Subject) спостерігає за погодою. Як тільки погодна умова змінюється, вона **сповіщає** **DayPlanner** (Observer), який автоматично перегенерує план.

## Запуск Проекту (Docker-Compose)

### Передумови
1.  Встановлено [Docker] та [Docker Compose].
2.  Ви маєте ключ API від [OpenWeatherMap].

### Кроки
1. **Запуск**
    ```bash
   python -m venv venv
   venv\Scripts\activate
   
   docker-compose up -d      
   docker-compose logs app -f                  
    ```

2. **Доступ до програми:**
    * **Frontend (UI):** `http://localhost:8080/`
    * **Backend (FastAPI Docs):** `http://localhost:8080/docs`
    * **MongoDB Admin (Mongo-Express):** `http://localhost:8081/`