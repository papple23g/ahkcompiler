//https://stackoverflow.com/questions/26360414/javascript-how-to-correct-indentation-in-html-string
function FormatHTML(str) {

    var div = document.createElement('div');
    div.innerHTML = str.trim();

    return FormatNode(div, 0).innerHTML;
}

function FormatNode(node, level) {

    var indentBefore = new Array(level++ + 1).join('  '),
        indentAfter = new Array(level - 1).join('  '),
        textNode;

    for (var i = 0; i < node.children.length; i++) {

        textNode = document.createTextNode('\n' + indentBefore);
        node.insertBefore(textNode, node.children[i]);

        FormatNode(node.children[i], level);

        if (node.lastElementChild == node.children[i]) {
            textNode = document.createTextNode('\n' + indentAfter);
            node.appendChild(textNode);
        }
    }

    return node;
}

//https://stackoverflow.com/questions/3665115/how-to-create-a-file-in-memory-for-user-to-download-but-not-through-server#answer-18197341
function DownloadTextFile(filename, text) {
    var element = document.createElement('a');
    text = text.replace(/\n/g, "\r\n"); //LT to CRLF https://stackoverflow.com/questions/3665115/how-to-create-a-file-in-memory-for-user-to-download-but-not-through-server#answer-18197341
    var universalBOM = "\uFEFF"; //utf-8 with bom https://stackoverflow.com/questions/42462764/javascript-export-csv-encoding-utf-8-issue
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(universalBOM + text));
    element.setAttribute('download', filename);
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
}