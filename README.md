# cadastre-bg-to-google-mymaps

Улеснява въвеждането на обекти от [Кадастрално-административна информационна система](kais.cadastre.bg) в Google My Maps. 
За мен това е полезно, защото Google My Maps може да се използва на телефон с GPS за да се установят приблизителните граници на обект (нива, парцел, т.н.).

## Употреба

Виж шаблона [input.yaml.example](input.yaml.example) за примерен входен документ с 2 обекта. Направи своя входен документ, като за всеки обект:

1. Попълни `name` (по избор, но в примера е формата който ми харесва) и `size` (площ в метри)
2. Попълни `edges`, като вземеш информацията от [Кадастрално-административна информационна система](kais.cadastre.bg)>Карта:

  Използвай търсенето в  за да намериш обекта, който те интересува. Избери координатна система `WGS UTM 35N`. После отвори конзолата на браузъра (`CTRL+SHIFT+K` във Firefox, `CTRL+SHIFT+J` в Chrome), напиши следната команда:

  > $('.ol-mouse-position').text().split(' ').slice(3).map(c => parseInt(c)).join(" ")

  Придвижи курсора на мишката върху един от ръбовете на обекта и натисни `Enter` за да изпълниш горната командата в конзолата. Това  което командата прави е да изведе координатите на този ръб в конзолата. Копирай тези координати на нов ред под `edges |`. После придвижи курсора на друг ръб (под ред, или по или обратно на часовниковата стрелка) и направи същото.



Когато попълниш входния файл, кръстен например `input.yaml`, изпълни следната команда:

> python create-mymaps-importable.py input.yaml output.kml

Ако всичко е наред, сега можеш да импортираш генерирания `output.kml` в Google My Maps - [инструкции](https://support.google.com/mymaps/answer/3024836?hl=en&ref_topic=3024924).
