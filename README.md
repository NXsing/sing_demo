# Simple interactive novel generator. Demo

## Запуск демки
1. Скачать(верхний правый угол страницы, зеленая кнопка)
2. Запустить index.html
3. [Посмотреть содержимое main.py]

## Базовый проект, для начала
https://github.com/NXsing/sing_basic

## Об API

Питоновые функции движка:
```python
r([название комнаты]) # начало блока комнаты
t(текст, [условие], [команда]) # текст
a(текст, команда, [условие]) # действие
e() # заверешние блока комнаты
```
Как видите, движок очень прост.

Есть еще "умная" функция `x(текст, [команда/условие])`, которая сама, на основе формата аргументов, вызывает t() или a(). Это позволяет писать код побыстрее.

## О движке

Питоновые функции(r,t,a,e) генерируют структуры, которые потом конвертируются в байт-код.

Байт-код потом интерпретируется в браузере, используя javascript.

Можно реализовать интерпретатор байт-кода и на любой-другой платформе(всего 15 инструкций). Сам байт-код(пока что) сохраняется в два файла: _bytes.js и bytes.pick

Файл bytes.pick можно импортировать в Питоне:
```python
import pickle
mem=pickle.load( open( "SOURCE/_bytes.pick", "rb" ) ) # байт-код прочитан
```
