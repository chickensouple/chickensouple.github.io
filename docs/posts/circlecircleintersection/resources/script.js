

function setup_pyodide(editor_text) {
    var imports_script = "import numpy as np; import matplotlib.pyplot as plt; import matplotlib.patches as mpatches; from js import document; import io; import base64;\n";

    jQuery.get("resources/draw_helpers_pyodide.py", 
        (text) => {
            var script = imports_script + editor_text + "\n" + text;
            pyodide.runPythonAsync(script)
                .then((output)=>{
                    console.log("Done");
                    $("#load-widget-div").css("visibility", "hidden");
                    $("#editor-io-div").css("visibility", "visible");
                    $("#loaded-widget-div").css("visibility", "visible");
                    $("#editor-outputarea").val(">>> Ready");
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

    var editor_text = editor.getSession().getValue();
    $("#load-widget-button1").click(() => {
        setup_pyodide(editor_text);
    });

    $("#editor-button1").click(() => {
        if ($("#load-widget-div").css("visibility") == "visible"){
            console.log("Pyodide not loaded yet.")
        } else {
            var editor_code = editor.getSession().getValue();
            $("#editor-outputarea").val(">>> Running Code");


            try {
            pyodide.runPythonAsync(editor_code + "\n" + "redraw_text()")
                .then((output)=>{
                    console.log(output);
                    $("#editor-outputarea").val(">>> Sucessfully Submitted");
                });
            } catch (error) {
                $("#editor-outputarea").val(">>> " + error);
            }
        }
    });

    // console.log($("#load-widget-div").css("visibility"))
    // console.log(editor.getSession().getValue());

    $("#widget-output").click((event) => {
        console.log(event.offsetX + ", " + event.offsetY);
    });

    window.addEventListener("resize", function() {
        resize_mathjax();  
    });
});
