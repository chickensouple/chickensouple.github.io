
$(document).ready(() => {

    // Ace Editor Stuff
    var editor = ace.edit("circle-editor");
    editor.getSession().setMode("ace/mode/python");
    editor.setTheme("ace/theme/monokai");

    var pyodide_setup_done = false;

    function run_circle_script() {
        jQuery.get("resources/draw_helpers_pyodide.py", function(textString) {
            pyodide.runPythonAsync(textString)
                .then((output)=>{pyodide_setup_done=true;})
                .catch((err)=>{console.log(err);});
        });
    };

    // Pyodide stuff
    languagePluginLoader.then(() => {
        setup_script = "import numpy as np; import matplotlib.pyplot as plt; import matplotlib.patches as mpatches; from js import document; import io; import base64;";
        pyodide.runPythonAsync(setup_script)
            .then((output)=>{run_circle_script()})
            .catch((err)=>{console.log(err);});
    });



});