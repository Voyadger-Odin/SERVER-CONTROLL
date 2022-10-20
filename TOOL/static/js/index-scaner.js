
//import * as cm from './context-menu.js';



document.oncontextmenu = function() {pageContextMenu(); return false;};


function httpGet(theUrl)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );
    return xmlHttp.responseText;
}

function httpPost(url, data)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "POST", url, true ); // false for synchronous request

    xmlHttp.onreadystatechange = function() {
        if (this.readyState != 4) return;
        return this.responseText
    }

    xmlHttp.send(data);

}

const params = new URLSearchParams(window.location.search)

let contextMenuOBJ;
let oldNameFile;


function deleteFile(){
    // Полное имя файла
    let name = contextMenuOBJ.getElementsByClassName('filename')[0].innerHTML
    oldNameFile = name
    $('#delete-file-name').html(name)
    $('#deleteFile').modal('show')
}
function deleteFileEvent(){
    // Полное имя файла
    let name = oldNameFile
    // Путь
    let path = params.get('path')

    let url = '/api/deletefile'
        + '?'
    + 'path=' + path
    + '&name=' + name;
    httpGet(url)

    location.reload()
}

function renameFile(){
    // Полное имя файла
    let name = contextMenuOBJ.getElementsByClassName('filename')[0].innerHTML
    oldNameFile = name
    $('#rename-file-name').val(name)
    $('#renameFile').modal('show')
}
function renameFileEvent(){
    // Полное имя файла
    let name = oldNameFile
    // Новое имя
    let newName = $('#rename-file-name').val()
    // Путь
    let path = params.get('path')

    let url = '/api/renamefile'
        + '?'
    + 'path=' + path
    + '&name=' + name
    + '&newname=' + newName;
    httpGet(url)

    location.reload()
}

function newDir(){
    $('#create-folder-name').val('')
    $('#createFolder').modal('show')
}
function createFolder(){
    let name = $('#create-folder-name').val()

    let url = '/api/createfolder'
        + '?'
    + 'path=' + params.get('path')
    + '&name=' + name;
    httpGet(url)

    location.reload()
}

function newFile(){
    $('#create-file-name').val('')
    $('#createFile').modal('show')
}
function newFileEvent(){
    // Новое имя
    let newName = $('#create-file-name').val()
    // Путь
    let path = params.get('path')

    let url = '/api/createfile'
        + '?'
    + 'path=' + path
    + '&name=' + newName;
    httpGet(url)

    location.reload()
}

function loadFiles(){
    $('#loadFiles').modal('show')
}
function loadFilesEvent(){
    // Путь
    let path = params.get('path')

    let url = 'api/uploadfile?path=' + path
    let fileBox = document.getElementById('formFileMultiple')
    let files = fileBox.files[0]

    console.log(files)

    let data = new FormData()
    data.append('files', files)
    //let resultSave = httpPost(url, data)
    //console.log(resultSave)


    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "POST", url, true ); // false for synchronous request

    xmlHttp.onreadystatechange = function() {
        if (this.readyState !== 4) return;

        if (this.responseText === 'ok'){
            location.reload()
        }
    }

    xmlHttp.send(data);
}

function scriptStart(){
    // Полное имя файла
    let name = contextMenuOBJ.getElementsByClassName('filename')[0].innerHTML
    // Путь
    let path = params.get('path')
    let fullName = path + '/' + name

    let url = '/cmd?fullName=' + fullName
    window.open(url);

}

function processWindow(){

    //getallprocess
    let url = '/api/getallprocess'
    let request = httpGet(url)
    let data = JSON.parse(request)
    let htmlConsoles = ''

    let console_data = ''
    let maxLines = 10

    if (data.length > 0){
         data.forEach((proces) => {

            url = '/api/getconsole?fullName=' + proces['console_path']
            //console_data = httpGet(url).replace(/\n/gi, '<br>')
            let console_data_array = httpGet(url).split('\n')
            console_data = ''
            for (let i=console_data_array.length - maxLines - 1; i < console_data_array.length; i++){
                if(i >= 0){
                    console_data += console_data_array[i] + '<br>'
                }
            }


            htmlConsoles += '<div class="mb-3 process" onclick="consoleOpen(\'' + proces['console_path'] + '\')">\n' +
                '                <div class="process-name"><center>' + proces['console_name'] + '</center></div>\n' +
                '<div class="process-text-box">' + console_data + '</div>' +
                '            </div>\n' +
                '              <br><br>'
        })

        $('#process-box').html(htmlConsoles)
    }
    $('#processWindow').modal('show')


}

function consoleOpen(path){
    let url = '/cmd?fullName=' + path
    window.open(url);
}

function uparchiv(){
    // Полное имя файла
    let name = contextMenuOBJ.getElementsByClassName('filename')[0].innerHTML
    // Путь
    let path = params.get('path')

    let url = '/api/uparchiv'
        + '?'
    + 'path=' + path
    + '&name=' + name;
    httpGet(url)

    location.reload()
}


function openFile(){
    // Полное имя файла
    let name = contextMenuOBJ.getElementsByClassName('filename')[0].innerHTML
    // Путь
    let path = params.get('path')
    //alert('open: ' + path + '/' + name)

    let url = '/editor' + '?'
    + 'path=' + path
    + '&name=' + name

    window.open(url);
}




function pageContextMenu(){
    if (contextMenuOBJ !== null){
        return false
    }

    let menu = [
        {
            'type': 'btn',
            'name': 'Новая папка',
            'img': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-folder-fill" viewBox="0 0 16 16">\n' +
        '  <path class="context-menu-btn" d="M9.828 3h3.982a2 2 0 0 1 1.992 2.181l-.637 7A2 2 0 0 1 13.174 14H2.825a2 2 0 0 1-1.991-1.819l-.637-7a1.99 1.99 0 0 1 .342-1.31L.5 3a2 2 0 0 1 2-2h3.672a2 2 0 0 1 1.414.586l.828.828A2 2 0 0 0 9.828 3zm-8.322.12C1.72 3.042 1.95 3 2.19 3h5.396l-.707-.707A1 1 0 0 0 6.172 2H2.5a1 1 0 0 0-1 .981l.006.139z"/>\n' +
        '</svg>',
            'onclick': 'newDir()'
        },
        {
            'type': 'btn',
            'name': 'Новый файл',
            'img': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-file-text" viewBox="0 0 16 16">\n' +
        '  <path class="context-menu-btn" d="M5 4a.5.5 0 0 0 0 1h6a.5.5 0 0 0 0-1H5zm-.5 2.5A.5.5 0 0 1 5 6h6a.5.5 0 0 1 0 1H5a.5.5 0 0 1-.5-.5zM5 8a.5.5 0 0 0 0 1h6a.5.5 0 0 0 0-1H5zm0 2a.5.5 0 0 0 0 1h3a.5.5 0 0 0 0-1H5z"/>\n' +
        '  <path class="context-menu-btn" d="M2 2a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V2zm10-1H4a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1z"/>\n' +
        '</svg>',
            'onclick': 'newFile()'
        },
        {
            'type': 'btn',
            'name': 'Загрузить',
            'img': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-cloud-arrow-up-fill" viewBox="0 0 16 16">\n' +
        '  <path class="context-menu-btn" d="M8 2a5.53 5.53 0 0 0-3.594 1.342c-.766.66-1.321 1.52-1.464 2.383C1.266 6.095 0 7.555 0 9.318 0 11.366 1.708 13 3.781 13h8.906C14.502 13 16 11.57 16 9.773c0-1.636-1.242-2.969-2.834-3.194C12.923 3.999 10.69 2 8 2zm2.354 5.146a.5.5 0 0 1-.708.708L8.5 6.707V10.5a.5.5 0 0 1-1 0V6.707L6.354 7.854a.5.5 0 1 1-.708-.708l2-2a.5.5 0 0 1 .708 0l2 2z"/>\n' +
        '</svg>',
            'onclick': 'loadFiles()'
        },
        {
            'type': 'line'
        },
        {
            'type': 'btn',
            'name': 'Процессы',
            'img': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-terminal-fill" viewBox="0 0 16 16">\n' +
                '  <path class="context-menu-btn" d="M0 3a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V3zm9.5 5.5h-3a.5.5 0 0 0 0 1h3a.5.5 0 0 0 0-1zm-6.354-.354a.5.5 0 1 0 .708.708l2-2a.5.5 0 0 0 0-.708l-2-2a.5.5 0 1 0-.708.708L4.793 6.5 3.146 8.146z"/>\n' +
                '</svg>',
            'onclick': 'processWindow()'
        },

    ];

    CreateContextMenu(menu);

    return false
}

function fileContextMenu(elem, type){
    contextMenuOBJ = elem

    // Полное имя файла
    let name = elem.getElementsByClassName('filename')[0].innerHTML
    // Расширение
    let fileType = name.split('.')[ name.split('.').length - 1 ]

    let menuEvent = []
    if (type === 'file'){
        menuEvent = [
            {
                'type': 'btn',
                'name': 'Открыть',
                'img': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pencil-square" viewBox="0 0 16 16">\n' +
                    '  <path class="context-menu-btn" d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z"/>\n' +
                    '  <path class="context-menu-btn" fill-rule="evenodd" d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5v11z"/>\n' +
                    '</svg>',
                'onclick': 'openFile()'
            },
        ]

        // Если скрипт, добавить кнопки запуска
        if (fileType === 'py'){
            menu2 = [
                {
                    'type': 'btn',
                    'name': 'Запустить',
                    'img': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-terminal-fill" viewBox="0 0 16 16">\n' +
                        '  <path class="context-menu-btn" d="M0 3a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V3zm9.5 5.5h-3a.5.5 0 0 0 0 1h3a.5.5 0 0 0 0-1zm-6.354-.354a.5.5 0 1 0 .708.708l2-2a.5.5 0 0 0 0-.708l-2-2a.5.5 0 1 0-.708.708L4.793 6.5 3.146 8.146z"/>\n' +
                        '</svg>',
                    'onclick': 'scriptStart()'
                },
            ];

            menuEvent = menu2.concat(menuEvent)
        }

        // Если архив, добавить кнопки разархивировать
        if (fileType === 'zip'){
            menu2 = [
                {
                    'type': 'btn',
                    'name': 'Разархивировать',
                    'img': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-file-earmark-zip-fill" viewBox="0 0 16 16">\n' +
                        '  <path class="context-menu-btn" d="M5.5 9.438V8.5h1v.938a1 1 0 0 0 .03.243l.4 1.598-.93.62-.93-.62.4-1.598a1 1 0 0 0 .03-.243z"/>\n' +
                        '  <path class="context-menu-btn" d="M9.293 0H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V4.707A1 1 0 0 0 13.707 4L10 .293A1 1 0 0 0 9.293 0zM9.5 3.5v-2l3 3h-2a1 1 0 0 1-1-1zm-4-.5V2h-1V1H6v1h1v1H6v1h1v1H6v1h1v1H5.5V6h-1V5h1V4h-1V3h1zm0 4.5h1a1 1 0 0 1 1 1v.938l.4 1.599a1 1 0 0 1-.416 1.074l-.93.62a1 1 0 0 1-1.109 0l-.93-.62a1 1 0 0 1-.415-1.074l.4-1.599V8.5a1 1 0 0 1 1-1z"/>\n' +
                        '</svg>',
                    'onclick': 'uparchiv()'
                },
            ];

            menuEvent = menu2
        }
    }else if (type === 'folder'){
        menuEvent = [
            {
                'type': 'btn',
                'name': 'Перейти',
                'img': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-folder2-open" viewBox="0 0 16 16">\n' +
                    '  <path class="context-menu-btn" d="M1 3.5A1.5 1.5 0 0 1 2.5 2h2.764c.958 0 1.76.56 2.311 1.184C7.985 3.648 8.48 4 9 4h4.5A1.5 1.5 0 0 1 15 5.5v.64c.57.265.94.876.856 1.546l-.64 5.124A2.5 2.5 0 0 1 12.733 15H3.266a2.5 2.5 0 0 1-2.481-2.19l-.64-5.124A1.5 1.5 0 0 1 1 6.14V3.5zM2 6h12v-.5a.5.5 0 0 0-.5-.5H9c-.964 0-1.71-.629-2.174-1.154C6.374 3.334 5.82 3 5.264 3H2.5a.5.5 0 0 0-.5.5V6zm-.367 1a.5.5 0 0 0-.496.562l.64 5.124A1.5 1.5 0 0 0 3.266 14h9.468a1.5 1.5 0 0 0 1.489-1.314l.64-5.124A.5.5 0 0 0 14.367 7H1.633z"/>\n' +
                    '</svg>',
                'onclick': 'folderClick(\'' + name + '\')'
            },
        ]
    }

    let menuedit = [
        {
            'type': 'btn',
            'name': 'Удалить',
            'img': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-archive-fill" viewBox="0 0 16 16">\n' +
        '  <path class="context-menu-btn" d="M12.643 15C13.979 15 15 13.845 15 12.5V5H1v7.5C1 13.845 2.021 15 3.357 15h9.286zM5.5 7h5a.5.5 0 0 1 0 1h-5a.5.5 0 0 1 0-1zM.8 1a.8.8 0 0 0-.8.8V3a.8.8 0 0 0 .8.8h14.4A.8.8 0 0 0 16 3V1.8a.8.8 0 0 0-.8-.8H.8z"/>\n' +
        '</svg>',
            'onclick': 'deleteFile()'
        },
        {
            'type': 'btn',
            'name': 'Переиминовать',
            'img': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pen-fill" viewBox="0 0 16 16">\n' +
        '  <path class="context-menu-btn" d="m13.498.795.149-.149a1.207 1.207 0 1 1 1.707 1.708l-.149.148a1.5 1.5 0 0 1-.059 2.059L4.854 14.854a.5.5 0 0 1-.233.131l-4 1a.5.5 0 0 1-.606-.606l1-4a.5.5 0 0 1 .131-.232l9.642-9.642a.5.5 0 0 0-.642.056L6.854 4.854a.5.5 0 1 1-.708-.708L9.44.854A1.5 1.5 0 0 1 11.5.796a1.5 1.5 0 0 1 1.998-.001z"/>\n' +
        '</svg>',
            'onclick': 'renameFile()'
        },

    ];

    let menu = menuEvent
        .concat([{'type': 'line'}])
        .concat(menuedit)


    CreateContextMenu(menu);

    return false
}

function folderClick(name){
    let path = '/';
    if (params !== null && params.has('path')){
        path = params.get('path') + '/'
    }

    let url = 'index.html' + '?' +
        'path=' + path + name
    window.location.replace(url);
}




document.addEventListener("DOMContentLoaded", function(){

    // отслеживаем нажатие мыши на странице
    $(document).mousedown(function(event) {
        // убираем наше контекстное меню со страницы
        if (event.target.id !== 'context-menu' && event.target.classList.contains('context-menu-btn') !== true){
            contextMenuOBJ = null;
            setTimeout(() => {  $('.context-menu').remove(); }, 10);
        }
    });
});