
const params = new URLSearchParams(window.location.search)
let editor;


function httpPost(url, data)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "POST", url, true ); // false for synchronous request
    xmlHttp.send(data);
    return xmlHttp.responseText;

}



document.addEventListener('keydown', e => {
    if (e.ctrlKey && e.key === 's') {
        // Prevent the Save dialog to open
        e.preventDefault();
        // Place your code here

        // Путь
        let path = params.get('path')
        let name = params.get('name')

        let url = 'http://127.0.0.1:5000/api/filesave'
            + '?'
            + 'path=' + path
            + '&name=' + name;

        //let data = '{"text": "url"}';
        let EditorText = editor.getValue()

        let data = new FormData()
        data.append('data', EditorText)

        let resultSave = httpPost(url, data)
        console.log(resultSave)
    }
});




window.onload = () => {
    CodeMirror.commands.autocomplete = function(cm) {
        cm.showHint({hint: CodeMirror.hint.anyword});
    }

    /*
    mode: 'python',
    mode: 'htmlmixed',
     */

    let file_name = params.get('name').split('.')
    let type = file_name[file_name.length - 1]

    let mode;
    if (type === 'html'){
        mode = {
                    name: "htmlmixed",
                    scriptTypes: [{matches: /\/x-handlebars-template|\/x-mustache/i,
                                   mode: null},
                                  {matches: /(text|application)\/(x-)?vb(a|script)/i,
                                   mode: "vbscript"}]
                  }
    }else if(type === 'py'){
        mode = 'python'
    }else if(type === 'css'){
        mode = 'css'
    } else if(type === 'js'){
        mode = 'javascript'
    }


    const input = document.getElementById('editor-area')
    editor = CodeMirror.fromTextArea(input,
        {
            viewportMargin: Infinity,
            styleActiveLine: true,
            matchBrackets: true,
            lineNumbers: true,
            lineWrapping: true,

            mode: mode,

            theme: "pastel-on-dark",
            scrollbarStyle: "overlay",
            extraKeys: {
                "Ctrl-F": "findPersistent",
                "Ctrl-Space": "autocomplete",
                "F11": function(cm) {
                  cm.setOption("fullScreen", !cm.getOption("fullScreen"));
                },
                "Esc": function(cm) {
                  if (cm.getOption("fullScreen")) cm.setOption("fullScreen", false);
                },
                "Ctrl-Q": function(cm){ cm.foldCode(cm.getCursor()); },
            },
            autoCloseBrackets: true,
            foldGutter: true,
            gutters: ["CodeMirror-linenumbers", "CodeMirror-foldgutter"],

        }
    )



    //editor.setMode('python')
}