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
