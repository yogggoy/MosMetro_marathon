Анимация маршрута Метромарафона от Яндекса.
===================

Подробнее о метромарафоне -   [Алгоритм Метромарафона.**habrahabr**](https://habrahabr.ru/company/yandex/blog/301030/)

маршрут Метромарафона - [Итоговый маршрут](https://docs.google.com/spreadsheets/d/1f1clOqt174ja8csqk6q3CjaXqk8H6Q_MxaP62ojWnls/pubhtml)

Список станций Московского метрополитена - [Википедия](https://ru.wikipedia.org/wiki/Список_станций_Московского_метрополитена)

----------

Зависимости
-------------

```
networkx    - построение графа "московского метро"
matplotlib  - визуализация
images2gif  - составление анимации (скачать с https://github.com/isaacgerg/images2gif)
```

структура

: draw_metro
: link_tables
: pars

render_gif

запуск
-------

Сначала нужно отрисовать каждый пункт маршрута в отдельный кадр, для этого запустите `draw_metro.py`  
После чего все кадры нужно собрать в GIF скриптом - `render_gif.py`

![](images.gif)
