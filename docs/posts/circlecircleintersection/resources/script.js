

function run_circle_script() {
    jQuery.get("resources/draw_helpers_pyodide.py", function(textString) {
        pyodide.runPythonAsync(textString)
            .then((output)=>{pyodide_setup_done=true;})
            .catch((err)=>{console.log(err);});
    });
};

function setup_pyodide() {
    var imports_script = "import numpy as np; import matplotlib.pyplot as plt; import matplotlib.patches as mpatches; from js import document; import io; import base64;\n";
    jQuery.get("resources/draw_helpers_pyodide.py", 
        (text) => {
            var script = var_import_script + text;
            pyodide.runPythonAsync(script)
                .then((output)=>{
                    console.log("Done");
                })
                .catch((err)=>{console.log(err);});
        });

}

function resize_mathjax() {
    var fontSize = Math.min(Math.max($(window).width() / 12, 70), 120);  
    var fontSizeStr = String(fontSize) + "%";

    jQuery('.MathJax').each(function(ii, obj) {
        obj.style.fontSize = fontSizeStr;
    });
}


$(document).ready(() => {
    // Ace Editor Stuff
    var editor = ace.edit("circle-editor");
    editor.getSession().setMode("ace/mode/python");
    editor.setTheme("ace/theme/monokai");

    $("#load_widget-button").click(() => {
        console.log("click");
        setup_pyodide();
    });

    // // Pyodide stuff
    // var pyodide_setup_done = false;

    // function run_circle_script() {
    //     jQuery.get("resources/draw_helpers_pyodide.py", function(textString) {
    //         pyodide.runPythonAsync(textString)
    //             .then((output)=>{pyodide_setup_done=true;})
    //             .catch((err)=>{console.log(err);});
    //     });
    // };
    // languagePluginLoader.then(() => {
    //     setup_script = "import numpy as np; import matplotlib.pyplot as plt; import matplotlib.patches as mpatches; from js import document; import io; import base64;";
    //     pyodide.runPythonAsync(setup_script)
    //         .then((output)=>{run_circle_script()})
    //         .catch((err)=>{console.log(err);});
    // });

    
    window.addEventListener("resize", function() {
        resize_mathjax();  
    });
});
