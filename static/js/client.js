function buyArt() {
    if (document.getElementById("terms").checked) {
        swal({
            title: "Are you sure?",
            text: "This image will be signed",
            type: "info",
            showCancelButton: true,
            closeOnConfirm: false,
            showLoaderOnConfirm: true
        },
            function () {
                let hashname = document.getElementById("hashname").value;
                let typeUser = document.getElementById("typeUser").value;
                let user = document.getElementById("user").value;
                $.ajax({
                    type: "POST",
                    url: "/picture",
                    data: {
                        hashname: hashname,
                        typeUser: typeUser,
                        user: user
                    },
                    cache: false,
                    success: function (response) {
                        if (response == "Purchase completed") {
                            swal({
                                title: "Process successful",
                                text: response,
                                type: "success"
                            },
                                function () {
                                    setTimeout(function () { location.href = "/artPublic"; }, 200);//Esperamos 0.2s para recargar la pagina
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
    } else {
        swal("Wait!", "You have to read our terms and conditions", "warning");
    }
    // let terms = document.getElementById("terms");
    // swal(terms);
}