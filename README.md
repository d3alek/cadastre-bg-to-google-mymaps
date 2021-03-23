# cadastre-bg-to-google-mymaps

Улеснява въвеждането на обекти от [Кадастрално-административна информационна система](kais.cadastre.bg) в Google My Maps. 
За мен това е полезно, защото Google My Maps може да се използва на телефон с GPS за да се установят приблизителните граници на обект (нива, парцел, т.н.).

## Изисквания

- proj: [инструкции](https://proj4.org/install.html)
- pyyaml: `pip install pyyaml`

## Употреба

### Входен документ
Добавяме обектите които ни интересуват във списъка (като ги намираме по някакъв начин и натискаме + до тях). После за да обработим всички във списъка изпълняваме следното в конзолата на Браузъра:

```
records = [];
printRecord = (number, label, data) => {
  record = `- name: ${label}\n`
  record += `  edges: |\n`;
  edges = data.split('((')[1].split('))')[0].split(',').map($.trim).map((d)=>d.split(' '))
  for (i = 0; i < edges.length; ++i) {
    wgs84 = proj4('EPSG:8122').inverse(edges[i])
    record += `    ${wgs84}\n`;
  }
  records.push(record);
}
objects = $('div#selectedList div.object')
for (i = 0; i < objects.length; ++i) {
  o = objects[i];
  id = $(o).find('.resultObjectId').attr('value')
  type = $(o).find('.resultObjectType').attr('value')
  subtype = $(o).find('.resultObjectSubType').attr('value')
  number = $(o).find('.resultObjectNumber').attr('value')
  label = $.trim($(o).find('.label').text())
  $.get(`https://kais.cadastre.bg/bg/Map/GetObjectGeometryByIdAndType/?id=${id}&type=${type}&subTypeId=${subtype}`, (data) => printRecord(number, label, data)).then(() => console.log('Done!'))
}
```

Като това свърши:

```
records.join('\n')
```

Това за сега взима само първите 10 запазени обекта.


### Генериране на изходен документ

Когато попълниш входния документ, кръстен например `input.yaml`, изпълни следната команда:

> python create-mymaps-importable.py -i input.yaml output.kml

Може вместо `-i input.yaml` да копираш входните данни и питонския скрипт ще ги намери.

Ако всичко е наред, сега можеш да импортираш генерирания `output.kml` в Google My Maps - [инструкции](https://support.google.com/mymaps/answer/3024836?hl=en&ref_topic=3024924).
