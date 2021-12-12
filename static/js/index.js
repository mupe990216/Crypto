function login() {
    let nick = document.getElementById("nickname");
    let pswd = document.getElementById("pswd");
    if (nick.value == "") {
        swal("Missing nickname", "", "error");
    } else if (pswd.value == "") {
        swal("Missing password", "", "error");
    } else {
        let dataJson = new Object();
        dataJson.usur = nick.value;
        dataJson.pswd = pswd.value;
        $.ajax({
            type: "POST",
            url: "/login",
            data: {
                dataJson: JSON.stringify(dataJson)
            },
            cache: false,
            success: function (response) {
                if (response == "Welcome!") {
                    swal({
                        title: "Welcome! on this website",
                        text: response,
                        type: "success"
                    },
                        function () {
                            setTimeout(function () { location.href = "/menu"; }, 350);//Esperamos 0.35s para recargar la pagina
                        });
                } else {
                    swal({
                        title: "Something went wrong",
                        text: response,
                        type: "error"
                    });
                }
            },
            error: function (response) { swal("Server Error", response); }
        })
    }
}

function register() {
    let cad = 0;
    let enviar = true;
    let form = document.getElementById("RegUsr");

    /* if (form.usur.value == "") {
        swal("Missing nickname", "", "error");
        enviar = false;
    } else {
        cad = form.usur.value.length;
        if (cad < 8) {
            swal("Nickname size", "minimum 8 characters", "error");
            enviar = false;
        }
    }
    
    if ((form.pswd1.value != form.pswd2.value) || (form.pswd1.value == "") || (form.pswd2.value == "")) {
        swal("Passwords do not match", "be careful!", "error");
        enviar = false;
    } else {
        cad = form.pswd1.value.length;
        if (cad < 8) {
            swal("Password size", "minimum 8 characters", "error");
            enviar = false;
        }
    }

    if(form.nombre.value == ""){
        swal("Missing name", "", "error");
        enviar = false;
    }else{
        cad = form.nombre.value.length;
        if (cad < 3) {
            swal("Name size", "minimum 3 characters", "error");
            enviar = false;
        }
    }

    if(form.ape1.value == ""){
        swal("Missing Surname", "", "error");
        enviar = false;
    }else{
        cad = form.ape1.value.length;
        if (cad < 3) {
            swal("Surname size", "minimum 3 characters", "error");
            enviar = false;
        }
    }

    if(form.ape2.value == ""){
        swal("Missing Surname", "", "error");
        enviar = false;
    }else{
        cad = form.ape2.value.length;
        if (cad < 3) {
            swal("Second surname size", "minimum 3 characters", "error");
            enviar = false;
        }
    }

    if(form.edad.value == ""){
        swal("Missing age", "", "error");
        enviar = false;
    }else{
        cad = form.edad.value;
        if(cad<18 || cad>99){
            swal("Age out of range", "Range: 18 - 99", "error");
            enviar = false;
        }
    }

    if (form.genero.value == -1){
        swal("Missing gender", "Select an option", "error");
        enviar = false;
    }
    
    if (form.userType.value == -1){
        swal("Missing user type", "Select an option", "error");
        enviar = false;
    }
    
    if(form.correo.value == ""){
        swal("Missing email", "", "error");
        enviar = false;
    } */

    if (enviar) {
        let dataJson = new Object();
        dataJson.usur = form.usur.value;
        dataJson.pswd = form.pswd1.value;
        dataJson.name = form.nombre.value;
        dataJson.ape1 = form.ape1.value;
        dataJson.ape2 = form.ape2.value;
        dataJson.age = form.edad.value;
        dataJson.gend = form.genero.value;
        dataJson.uTyp = form.userType.value;
        dataJson.email = form.correo.value;
        swal({
            title: "Are you sure?",
            text: "Please wait",
            type: "info",
            showCancelButton: true,
            closeOnConfirm: false,
            showLoaderOnConfirm: true
        },
            function () {
                $.ajax({
                    type: "POST",
                    url: "/register",
                    data: {
                        dataJson: JSON.stringify(dataJson)
                    },
                    cache: false,
                    success: function (response) {
                        if (response == "Registration successful!") {
                            swal({
                                title: "Registration successful",
                                text: response,
                                type: "success"
                            },
                                function () {
                                    setTimeout(function () { location.href = "/"; }, 350);//Esperamos 0.35s para recargar la pagina
                                });
                        } else {
                            swal({
                                title: "Something went wrong",
                                text: response,
                                type: "error"
                            });
                        }
                    },
                    error: function (response) { swal("Server Error", response); }
                })
            }
        );
    }

}