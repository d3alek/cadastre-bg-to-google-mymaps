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
records = {};
printRecord = (number) => {
  record = `- name: ${records[number]['label']}\n`
  record += `  description: ${records[number]['description']}\n`;
  record += `  edges: |\n`;
  edges = records[number]['data'].split('((')[1].split('))')[0].split(',').map($.trim).map((d)=>d.split(' '))
  for (i = 0; i < edges.length; ++i) {
    wgs84 = proj4('EPSG:8122').inverse(edges[i])
    record += `    ${wgs84}\n`;
  }
  return record;
}
processData = (number) => (data) => {
  records[number]['data'] = data
}
processDescription = (number) => (data) => {
  records[number]['description'] = data
}
printRecords = () => {
  console.log('! For clipboard copy to work, interact with the map now');
  setTimeout(async () => {
    printed = ""
    for (record in records) {
      printed += printRecord(record)
    }
    console.log(printed);
    navigator.clipboard.writeText(printed).then(function() {
      console.log("Copied to clipboard successfully!");
    }, function(err) {
      console.error("Unable to write to clipboard.", err);
    });
  }, 2000);
}
objects = $('div#selectedList div.object')
for (i = 0; i < objects.length; ++i) {
  o = objects[i];
  id = $(o).find('.resultObjectId').attr('value')
  type = $(o).find('.resultObjectType').attr('value')
  subtype = $(o).find('.resultObjectSubType').attr('value')
  number = $(o).find('.resultObjectNumber').attr('value')
  label = $.trim($(o).find('.label').text())
  records[number] = {}
  records[number]['label'] = label;
  $.get(`https://kais.cadastre.bg/bg/Map/GetObjectGeometryByIdAndType/?id=${id}&type=${type}&subTypeId=${subtype}`, processData(number))
  $.get(`https://kais.cadastre.bg/bg/Map/GetObjectInfo/?id=${id}&type=${type}&subTypeId=${subtype}&number=NaN`, processDescription(number))
}
```

Като това свърши:

```
printRecords()

```

Това за сега взима само първите 10 запазени обекта. Опитва да ги копира автоматично (ако изпише `Copied to clipboard successfully!` значи е успяло), така че да можеш направо да ги поставиш (Paste) в `input.yaml`.


### Генериране на изходен документ

Когато попълниш входния документ, кръстен например `input.yaml`, изпълни следната команда:

> python create-mymaps-importable.py -i input.yaml output.kml

Може вместо `-i input.yaml` да копираш входните данни и питонския скрипт ще ги намери.

Ако всичко е наред, сега можеш да импортираш генерирания `output.kml` в Google My Maps - [инструкции](https://support.google.com/mymaps/answer/3024836?hl=en&ref_topic=3024924).
