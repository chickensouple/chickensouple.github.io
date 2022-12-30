

function setup_pyodide(load_widget_button_id, load_widget_div_id,
    loaded_widget_div_id, hidden_script, initial_editor_text) {
    var imports_script = "import numpy as np; import matplotlib.pyplot as plt; import matplotlib.patches as mpatches; from js import document; import io; import base64;\n";


    $(load_widget_button_id).click(() => {
        jQuery.get(hidden_script,
            (text) => {
                var script = imports_script + initial_editor_text + "\n" + text;
                pyodide.runPythonAsync(script)
                    .then((output) => {
                        console.log("Done");
                        $(load_widget_div_id).css("visibility", "hidden");
                        $("#editor-io-div").css("visibility", "visible");
                        $(loaded_widget_div_id).css("visibility", "visible");
                        $("#editor-outputarea").text("Ready");
                    })
                    .catch((err) => { console.log(err); });
            });
    });


}

