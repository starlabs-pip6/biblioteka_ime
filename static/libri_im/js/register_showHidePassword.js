function showhide() {

    var type = document.getElementById("password").getAttribute("type");
   

    if (type == "password")
    {
        //Change type attribute
        document.getElementById("password").setAttribute("type", "text");


    } else
    {
        //Change type attribute
        document.getElementById("password").setAttribute("type", "password");
    }

}
function showhide1(){
    var type = document.getElementById("password1").getAttribute("type");
    if (type == "password")
    {
        //Change type attribute
        document.getElementById("password1").setAttribute("type", "text");


    } else
    {
        //Change type attribute
        document.getElementById("password1").setAttribute("type", "password");
    }

}

