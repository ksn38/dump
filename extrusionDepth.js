(function renameLayerSource() {
    app.beginUndoGroup("Rename Layer Source");
    var myComp = app.project.activeItem;
    var layers = ["Argentina", "Belize", "Bolivia", "Brazil", "Chile", 
    "Colombia", "Costa Rica", "Cuba", "Dominican Republic", "Ecuador", 
    "El Salvador", "France", "Guatemala", "Guyana", "Haiti", "Honduras", 
    "Jamaica", "Mexico", "Nicaragua", "Panama", "Paraguay", "Peru", 
    "Suriname", "Uruguay", "Venezuela, RB"];
        
    for (var i = 0; i < layers.length; i++){
        //var newName = prompt("print Outlines", layers[i]);
        var chkLayer = myComp.layer(layers[i] + " Outlines");
        chkLayer.geometryOption.extrusionDepth.expression = ('x = thisComp.layer("la.mgjson")("Data")("Outline")("' + layers[i] + '");\
slider = (thisComp.layer("slider height").transform.position[0])/10;\
x*slider');
    }
    //var newName = prompt("Rename Layer Source");
    app.endUndoGroup();
})();
