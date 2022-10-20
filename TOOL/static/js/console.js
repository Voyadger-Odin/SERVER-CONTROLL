

const params = new URLSearchParams(window.location.search)


function httpGet(theUrl)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );
    return xmlHttp.responseText;
}

let consolePanel;
let SCRIPT_END = '{{SCRIPT END}}'


function StopScript(){
    let fullName = params.get('fullName')
    let url = '/api/stopscript?fullName=' + fullName
    data = httpGet(url)
    //alert('STOP')
}


let scriptRuning = true
function getConsole(){
    // файл
    let fullName = params.get('fullName')
    let url = '/api/getconsole?fullName=' + fullName
    let data = ''
    if (scriptRuning){
        data = httpGet(url)

        if (data !== SCRIPT_END){
            consolePanel.setValue(data)
            consolePanel.setCursor(data.length);
        }else{
            scriptRuning = false
        }
    }
}

function update(){
    //console.log('cmd')
    getConsole();
    // Добавить текст в конец.
    //$('#console-panel').val($.trim($('#console-panel').val() + '\n' + 'Текст в конце.'));
}

function timer(){
    update();
    setTimeout(timer, 1000);
}


window.onload = () => {

    const input = document.getElementById('console-panel')
    consolePanel = CodeMirror.fromTextArea(input,
        {
            theme: 'tomorrow-night-bright',
            scrollbarStyle: 'overlay',
            lineWrapping: true,
        }
    )

    timer()
}