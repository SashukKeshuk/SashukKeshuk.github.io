# NDV (Non-Disclosure Violation)

### План тестирования:
1) поиск sensitive info
2) поиск нелицинзированных зависимостей
3) анализ исходящего трафика


# Поиск чувствительной информации:

Цель: найти утечку чувствительной информации в исходниках / конфигах / метаданных.
Инструменты: GitGuardian, SecretFinder, ExifTool

## Поиск секретов, чувствительных данных:

### SecretFinder:
1) Установка:
```
git clone https://github.com/m4ll0k/SecretFinder.git secretfinder
cd secretfinder
# Создаем / активируем venv если надо
python -m pip install -r requirements.txt or pip install -r requirements.txt
```
2) Сканирование:

- Входим в директорию сканируемого проекта
- \<\<PATH\>\> - путь до secretfinder

js: `find . -type f -name "*.js" | while read js_file; do python3 <<PATH>>/SecretFinder.py -i "$js_file" -o cli; done` 
py: `find . -type f -name "*.py" | while read py_file; do python3 <<PATH>>/SecretFinder.py -i "$py_file" -o cli; done` 
log: `find . -type f -name "*.log" | while read log_file; do python3 <<PATH>>/SecretFinder.py -i "$log_file" -o cli; done`
cfg: `find . -type f -name "*.cfg" | while read cfg_file; do python3 <<PATH>>/SecretFinder.py -i "$cfg_file" -o cli; done` 
ini: `find . -type f -name "*.ini" | while read ini_file; do python3 <<PATH>>/SecretFinder.py -i "$ini_file" -o cli; done` 

Остальные файлы: `python3 SecretFinder.py -i . -o cli -r -g 'js;py;log;cfg;ini'`

Анализируем вывод **ПОСЛЕ КАЖДОЙ КОМАНДЫ**<br>
Разбиваем скан пофайлово т.к. инструмент лучше анализирует каждый файл по отельности (мелкими порциями) и для удобства анализа.


### GitGuard
1) Установка (через pipx):
```
pipx install ggshield
pipx upgrade ggshield
```

2) Сканирование:

Входим в директориб проекта
- `ggshield secret scan path -r .` (по исходникам)
- `ggshield secret scan docker image:tag` (по образу)
- `ggshield secret scan commit-range --from=first-commit --to=HEAD` (история коммитов) важно быть в директории проекта т.к. путь явно не указывается

Ручной анализ результата


### Ручной анализ исходников:

- Смотрим основные конфиг файлы и верхушки программных файлов.
- Проверяем докер файлы
- Проверяем историю гит вручную `git log -p | grep -E '(?i)(api[_-]?key|token|secret|password)'`
- Проверяем метаинформацию в png, jpeg, mp4, mp3, pdf, pptx, odt, rar, zip, svg, подозрительных html файлых с помощью exiftool: `exiftool file`


# Поиск зависимостей

Цель: найти нелицензированные зависимости, нарушающие соглашение о неразглашении (NDA)
Инструменты: license-checker (Node.js), pip-licenser (Python), license (Java), scancode-toolkit

Для **Node.js** проектов:
```
# Устновка
npm install -g license-checker

# Запуск
license-checker --json --out licenses.json
jq . licenses.json
```

Для **Python** проектов:
```
# Установка
pip install pip-licenses

# Запуск
pip-licenses --format=json --output-file=licenses.json
jq . licenses.json
```


Для **Java** проектов:
```
mvn license:download-licenses
```


После (для любых яп) используем scancode-toolkit для транзитивных зависимостей.
Для ее работы необходимы модули icu-i18n, icu-config. Проверяем командами `pkg-config --modversion icu-i18n` и `icu-config --version`.
Если нету то устанавливаем через apt и **в конце выполняем apt upgrade**.

Устанавливаем scancode-toolkit: `pip install scancode-toolkit`
Сканируем с сохранением результатат в json (анализ на этйо стадии не нужен)
```
scancode --license --package --json-pp scancode_results.json .
```
