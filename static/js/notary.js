function signContract() {
    if (document.getElementById("terms").checked) {
        swal({
            title: "Are you sure?",
            text: "This contract will be signed",
            type: "info",
            showCancelButton: true,
            closeOnConfirm: false,
            showLoaderOnConfirm: true
        },
            function () {
                let userArtist = document.getElementById("userArtist").value;
                let userClient = document.getElementById("userClient").value;
                let userPnotar = document.getElementById("userPnotar").value;
                let hashname = document.getElementById("hashname").value;
                let emailArtist = document.getElementById("emailArtist").value;
                let emailClient = document.getElementById("emailClient").value;
                let emailPnotar = document.getElementById("emailPnotar").value;
                let typeUser = document.getElementById("typeUser").value;
                let idPreCont = document.getElementById("idPreCont").value;
                let dataJson = new Object();
                dataJson.userArtist = userArtist;
                dataJson.userClient = userClient;
                dataJson.userPnotar = userPnotar;
                dataJson.hashname = hashname;
                dataJson.emailArtist = emailArtist;
                dataJson.emailClient = emailClient;
                dataJson.emailPnotar = emailPnotar;
                dataJson.idPreCont = idPreCont;
                $.ajax({
                    type: "POST",
                    url: "/picture",
                    data: {
                        hashname: hashname,
                        typeUser: typeUser,
                        dataJson: JSON.stringify(dataJson)
                    },
                    cache: false,
                    success: function (response) {
                        if (response == "Signed contract") {
                            swal({
                                title: "Process successful",
                                text: response,
                                type: "success"
                            },
                                function () {
                                    setTimeout(function () { location.href = "/contracts"; }, 200);//Esperamos 0.2s para recargar la pagina
                                });
                        } else {
                            swal({
                                title: "Something went wrong",
                                text: response,
                                type: "error"
                            },
                                function () {
                                    setTimeout(function () { location.href = "/contracts"; }, 200);//Esperamos 0.2s para recargar la pagina
                                });
                        }
                    },
                    error: function (response) { swal("Server Error", response); }
                })
            }
        );
    } else {
        swal("Wait!", "You have to read our terms and conditions", "warning");
    }
    // let terms = document.getElementById("terms");
    // swal(terms);
}