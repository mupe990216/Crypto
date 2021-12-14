function verify() {
    let imgFile = document.getElementById('imageFile');
    let title = document.getElementById('title').value;
    if ( (imgFile.value != "")) {
        swal({
            title: "Are you sure?",
            text: "This image will be uploaded",
            type: "info",
            showCancelButton: true,
            closeOnConfirm: false,
            showLoaderOnConfirm: true
        },
            function () {
                let formData = new FormData(); // Objeto donde se enviara toda la info
                let imageFile = $('#imageFile')[0].files[0]; // Se extra la imagen a mandar
                formData.append('imageFile', imageFile); //Se agrega al objeto
                let dataJson = new Object(); //Se crea un objeto para guardar el texto 
                dataJson.title = title; //Se asigan los valores a cada key
                formData.append('title', JSON.stringify(dataJson)); //Se serializa el objeto texto con el de imagen
                $.ajax({
                    type: "POST",
                    url: "/CheckSigns",
                    data: formData,
                    cache: false,
                    contentType: false,
                    processData: false,
                    success: function (response) {
                        if (response == "Digital signatures match") {
                            swal({
                                title: "Image Correct!",
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
                            });
                        }
                    },
                    error: function (response) { swal("Server Error", response); }
                })
            }
        );
    } else {
        swal("Filed empty", "Select the image of your contract", "error");
    }
}