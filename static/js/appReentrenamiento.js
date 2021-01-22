
    

	function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var contenedor=document.getElementById('contenedor_carga');     
const csrftoken = getCookie('csrftoken');
var formData = new FormData();

        $(document).on('submit', '#reentrenar', function(e) 
        {
             e.preventDefault();
           contenedor.style.visibility="visible";
            formData.append('numFiltro1', $('#numFiltro1').val())
            formData.append('numFiltro2', $('#numFiltro2').val())
            formData.append('numEpocas', $('#numEpocas').val())
            formData.append('csrfmiddlewaretoken', csrftoken)

            $.ajax({
                
                type: 'POST',
                url: 'reentrenar_red_neuronal',
                data: formData,
                cache: false,
                processData: false,
                contentType: false,
                enctype: 'multipart/form-data',
                success: function (response){

                if(response.id_reentrenamiento !=null){
                var ruta="cargar_reporte_reentrenamiento".concat(response.id_reentrenamiento)  
                }else{
                var ruta="reentrenamiento"
                }
                window.location.replace(ruta);
                },
                error: function(xhr, errmsg, err) {
                    console.log(xhr.status + ":" + xhr.responseText)
                    window.location.replace("reentrenamiento");
                }
            })
         
            
        })



