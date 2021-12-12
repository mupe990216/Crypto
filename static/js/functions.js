/**
 * Esta funcion es llamada en "artist_index.html" como respuesta GET de la ruta /upload
 * Sirve para previsualizar una imagen que esta a punto de ser subida al servidor de imagenes
 * 
 */
function validarExt() {
    let archivoInput = document.getElementById('imageFile');
    let archivoRuta = archivoInput.value;
    let extPermitidas = /(.jpg|.png|.jpeg)$/i;
    if (!extPermitidas.exec(archivoRuta)) {
        swal("Denied!", "Select a valid image", "error");
        archivoInput.value = '';
        let imagetest = document.getElementById('imagetest');
        if (imagetest != null) {
            imagetest.src = '';
        }
        return false;
    } else {
        //PRevio del PDF
        if (archivoInput.files && archivoInput.files[0]) {
            let visor = new FileReader();
            visor.onload = function (e) {
                document.getElementById('visorArchivo').innerHTML =
                    '<embed id="imagetest" src="' + e.target.result + '" width="400" style="height: auto; object-fit: cover; object-position: center center;" />';
            };
            visor.readAsDataURL(archivoInput.files[0]);
        }
    }
}

/**
 * Esta funcion envia la imagen llamada en "artist_index.html" como peticion POST a la ruta /upload
 */
function sendImage() {
    let imgFile = document.getElementById('imageFile');
    if (imgFile.value != "") {
        swal({
            title: "Are you sure?",
            text: "This image will be uploaded",
            type: "info",
            showCancelButton: true,
            closeOnConfirm: false,
            showLoaderOnConfirm: true
        },
            function () {
                let formData = new FormData();
                let imageFile = $('#imageFile')[0].files[0];
                formData.append('imageFile', imageFile);
                $.ajax({
                    type: "POST",
                    url: "/upload",
                    data: formData,
                    cache: false,
                    contentType: false,
                    processData: false,
                    success: function (response) {
                        if (response == "Art stored") {
                            swal({
                                title: "Stored successful",
                                text: response,
                                type: "success"
                            },
                                function () {
                                    setTimeout(function () { location.href = "/upload"; }, 200);//Esperamos 0.2s para recargar la pagina
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
        swal("Filed empty", "Select an image", "error");
    }
}