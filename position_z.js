(function renameLayerSource() {
    app.beginUndoGroup("Rename Layer Source");
    var myComp = app.project.activeItem;
    var layers = ["Argentina", "Belize", "Bolivia", "Brazil", "Chile", 
    "Colombia", "Costa Rica", "Cuba", "Dominican Republic", "Ecuador", 
    "El Salvador", "France", "Guatemala", "Guyana", "Haiti", "Honduras", 
    "Jamaica", "Mexico", "Nicaragua", "Panama", "Paraguay", "Peru", 
    "Suriname", "Uruguay", "Venezuela, RB"];
        
    for (var i = 0; i < layers.length; i++){
        //var newName = prompt("print", layers[i]);
        var chkLayer = myComp.layer(layers[i] + " Outlines");
        chkLayer.property("Position").expression = ('h = thisComp.layer("la.mgjson")("Data")("Outline")("' + layers[i] + '");\
slider = (thisComp.layer("slider height").transform.position[0])/10;\
z = 0;\
if (h < 0){\
    z = h*slider;\
}\
[value[0], value[1], z];');
    }
    //var newName = prompt("Rename Layer Source");
    app.endUndoGroup();
})();

