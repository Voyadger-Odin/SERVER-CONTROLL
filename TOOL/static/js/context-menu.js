

function test_import(){
    alert('ok');
}

function CloseContextMenu(){
    setTimeout(() => {  $('.context-menu').remove(); }, 10);
}

function CreateContextMenu(menu){
    //console.log(menu)


    let menuHTML = '';

    menuHTML = '<table>';

    menu.forEach(function (item){
        //console.log(item);
        if (item['type'] === 'btn'){
            menuHTML += '<tr onclick="' + item['onclick'] + ';CloseContextMenu()">' +
                '<td class="context-menu-btn">' + item['img'] + '</td>' +
                '<td class="context-menu-btn">' + item['name'] + '</td>' +
                '</tr>';
        }

        if (item['type'] === 'line'){
            menuHTML += '<tr class="context-menu-line"></tr>';
        }
    });
    menuHTML += '</table>';

    // создаём новый блок, в котором будет наше меню
    $('<div/>', {
        // назначаем ему свой класс, описанный в стилях, чтобы блок появился на странице
      class: 'context-menu',
        id: 'context-menu'
    })
    .css({
        // получаем координаты клика и делаем их координатами меню
      left: event.pageX+'px',
      top: event.pageY+'px'
    })
    // добавляем блок на страницу
    .appendTo('body')
    // и добавляем пункты в новое контекстное меню
    .append(menuHTML).show();
}