# Nenets Verb Lemmatizer

Программа для лемматизации ненецких глагольных форм.

## Что внутри
- `lemmatizer_app/core.py` — ядро лемматизации без зависимостей от словаря;
- `lemmatizer_app/views.py` — web/UI и JSON API;
- `lemmatizer_app/templates/` — минимальный интерфейс;
- `docs/linguistic_basis.md` — происхождение правил, лингвистическая база и границы реализации.

## Лингвистическая основа
- текущая версия продолжает более ранние исследовательские материалы по лемматизации ненецких глаголов;
- правила основаны на анализе глагольных суффиксов, типов спряжения и нормализации написания;
- исторические материалы сохранены в `legacy/`, но объектом регистрации является текущая самостоятельная программа.

## Запуск
```bash
cd /Users/paul/PyCharmProjects/GitHub/nenets_verb_lemmatizer
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py check
python manage.py runserver 127.0.0.1:8010
```

Открыть:
- `http://127.0.0.1:8010/`
- `http://127.0.0.1:8010/api/lemmatize/?text=тарпыдинзь`

## Архив для Роспатента
```bash
cd /Users/paul/PyCharmProjects/GitHub/dictionary-rus-nen/nenets_verb_lemmatizer
./scripts/build_submission_zip.sh
```

Скрипт собирает архив в `dist/` без `.git`, `__pycache__`, локальной базы и служебного мусора.
