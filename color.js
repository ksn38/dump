(function renameLayerSource() {
    app.beginUndoGroup("Rename Layer Source");
    var myComp = app.project.activeItem;
    var layers = ["Argentina", "Belize", "Bolivia", "Brazil", "Chile", 
    "Colombia", "Costa Rica", "Cuba", "Dominican Republic", "Ecuador", 
    "El Salvador", "France", "Guatemala", "Guyana", "Haiti", "Honduras", 
    "Jamaica", "Mexico", "Nicaragua", "Panama", "Paraguay", "Peru", 
    "Suriname", "Uruguay", "Venezuela, RB"];
        
    for (var i = 0; i < layers.length; i++){
        //prompt("Layer Outlines", layers[i]);
        var chkLayer = myComp.layer(layers[i] + " Outlines");
        chkLayer.content("Group 1").content("Fill 1").property('Color').expression = ('x = thisComp.layer("la.mgjson")("Data")("Outline")("' + layers[i] + '");\
slider = (thisComp.layer("slider").transform.position[0])/10;\
z = 0;\
if (x>0){\
	[0, x*slider, 0, 0]/255\
}\
else{\
	[Math.abs(x)*slider, 0, 0, 0]/255\
}');
    }
    //var newName = prompt("Rename Layer Source");
    app.endUndoGroup();
})();
