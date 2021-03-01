
var editor = ace.edit("editor");
editor.getSession().setMode("ace/mode/python");
editor.setTheme("ace/theme/monokai");
languagePluginLoader.then(() => { $("#output").val("Ready\n>>>"); });

$("#button").click(function() {
pyodide.runPythonAsync(editor.getValue())
    .then(function(output) {$("#output").val($("#output").val() + "\n>>>" + String(output));})
    .catch(function(err) {$("#output").val($("#output").val() + "\n>>>" + String(err));});
});