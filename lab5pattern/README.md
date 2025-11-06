# SmartApp IoT — Microservices Example

## Опис
Проект, що демонструє мікросервісну архітектуру для Smart Home:
- Головний вебзастосунок (FastAPI) на порту **8000**
- Пристрої як окремі мікросервіси:
  - Smart Speaker — порт **8001**
  - Smart Light — порт **8002**
  - Smart Curtains — порт **8003**

Головний додаток використовує патерни **Controller** і **Facade** для взаємодії з пристроями.
Також продемонстровано **Decorator** (LoggingDeviceDecorator) як приклад додавання логування.

## Файли
- `main.py` — головний вебзастосунок (UI)
- `controller/` — логіка контролера і фасад для HTTP-запитів до пристроїв
- `devices/` — реалізації пристроїв (кожен — окремий FastAPI сервіс)
- `web/templates/index.html`, `web/static/style.css` — UI

## Запуск 
1. Встанови залежності:
   ```bash
   pip install -r requirements.txt
2. Термінал 1: speaker
   ```bash
   python -m devices.smart_speaker
3. Термінал 2: light
   ```bash
   python -m devices.smart_light
4. Термінал 3: curtains
   ```bash
   python -m devices.smart_curtains
5. Термінал 4: main dashboard
   ```bash
   python -m main
