(function renameLayerSource() {
    app.beginUndoGroup("Rename Layer Source");
    var myComp = app.project.activeItem;
    var layers = ["Afghanistan Outlines", "Armenia Outlines", 
    "Azerbaijan Outlines", "Bangladesh Outlines", "Bhutan Outlines", 
    "Brunei Darussalam Outlines", "Cambodia Outlines", "China Outlines", 
    "Cyprus Outlines", "Egypt, Arab Rep Outlines", "Georgia Outlines", 
    "India Outlines", "Indonesia Outlines", "Iran, Islamic Rep Outlines", 
    "Iraq Outlines", "Israel Outlines", "Japan Outlines", "Jordan Outlines", 
    "Kazakhstan Outlines", "Kuwait Outlines", "Kyrgyz Republic Outlines", 
    "Lao PDR Outlines", "Lebanon Outlines", "Malaysia Outlines", "Mongolia Outlines", 
    "Myanmar Outlines", "Nepal Outlines", "Korea, Dem Outlines", 
    "Oman Outlines", "Pakistan Outlines", "Philippines Outlines", "Russian Federation Outlines", 
    "Qatar Outlines", "Saudi Arabia Outlines", "Singapore Outlines", 
    "Korea, Rep Outlines", "Sri Lanka Outlines", "Syrian Arab Republic Outlines", 
    "Tajikistan Outlines", "Thailand Outlines", "Timor-Leste Outlines", 
    "Turkmenistan Outlines", "Turkiye Outlines", "United Arab Emirates Outlines", 
    "Uzbekistan Outlines", "Viet Nam Outlines", "Yemen, Rep Outlines"];
        
    for (var i = 0; i < layers.length; i++){
        //var newName = prompt("print Outlines", layers[i]);
        var chkLayer = myComp.layer(layers[i]);
        chkLayer.content("Group 1").content("Fill 1").property('Color').expression = ('x = thisComp.layer("asia.mgjson")("Data")("Outline")("' + layers[i].slice(0,-9) + '");\
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
