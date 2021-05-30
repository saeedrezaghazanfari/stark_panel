
function getContent_editor(){
    document.getElementById("pk-editor-my-textarea").value = document.getElementById("pk-editor-area").innerHTML;
}
function save() {
    getContent_editor();
    // document.getElementById("pk-editor-save").submit();
}
function changeFont(){
    var myFont = document.getElementById("pk-editor-input-font").value;
    document.execCommand('fontName', false, myFont);
}
function checkDiv(){
    var editorText = document.getElementById("pk-editor-area").innerHTML;
    if(editorText === ''){
        document.getElementById("pk-editor-area").style.border = '5px solid red';
    }
}
function removeBorder(){
    document.getElementById("pk-editor-area").style.border = '1px solid transparent';
} 

function getContent_editor(){
    document.getElementById("pk-editor-my-textarea").value = document.getElementById("pk-editor-area").innerHTML;
}
function save() {
    getContent_editor();
    // document.getElementById("pk-editor-save").submit();
}