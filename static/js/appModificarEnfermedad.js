document.addEventListener('DOMContentLoaded', function() {

var filesEntrenamiento=[];
var filesValidacion=[];
var filesMuestra=[];

document.getElementById("fileEntrenamiento").addEventListener("change", function(event) {
  let output = document.getElementById("numeroArchivosEntrenamiento");
  filesEntrenamiento = event.target.files;
  filesEntrenamiento=limpiarArchivos(filesEntrenamiento);

  var txt="";
  filesEntrenamiento.length==1 ? txt=" Imágen cargada": txt=" Imágenes cargadas";
  output.innerHTML=String(filesEntrenamiento.length).concat(txt);
}, 
false);

document.getElementById("fileValidacion").addEventListener("change", function(event) {
  let output = document.getElementById("numeroArchivosValidacion");
  filesValidacion = event.target.files;
  filesValidacion=limpiarArchivos(filesValidacion);
  var txt="";
  filesValidacion.length==1 ? txt=" Imágen cargada": txt=" Imágenes cargadas";
  output.innerHTML=String(filesValidacion.length).concat(txt);
}, 
false);

function limpiarArchivos(files){
var imagenes=[];
  const validImageTypes = ['image/jpeg', 'image/png'];
    for (let i=0; i<files.length; i++) {
if (validImageTypes.includes(files[i].type)) {
    imagenes.push(files[i])
  }  
}
 return imagenes;
}

 FilePond.registerPlugin(FilePondPluginFileValidateSize);
        FilePond.registerPlugin(FilePondPluginFileValidateType);
        FilePond.setOptions({
            allowMultiple:true,
        
        })
        const inputElement = document.getElementById('filesMuestra');
        const pond = FilePond.create( inputElement, {
            acceptedFileTypes:['image/png', 'image/jpeg'],
            onaddfile: (err, fileItem) => {
                if (!err) {
                filesMuestra.push(fileItem.file)
                }
  
            },
            onremovefile: (err, fileItem) => {
                const index = filesMuestra.indexOf(fileItem.file)
                if (index > -1) {
                    filesMuestra.splice(index, 1)
                }
      
            }
        } );

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
    

const csrftoken = getCookie('csrftoken');
var formData = new FormData();
         
        $(document).on('submit', '#modificarMuestra', function(e) 
        {
    
             e.preventDefault();
            for (var i = 0; i < filesMuestra.length; i++) 
            {
                formData.append('muestra' + i, filesMuestra[i])
            }

            formData.append('lengthMuestra', filesMuestra.length)
            formData.append('idEnfermedad',idEnfermedad)
            formData.append('csrfmiddlewaretoken', csrftoken)

            $.ajax({
                
                type: 'POST',
                url: 'modificar_imagenes_muestra',
                data: formData,
                cache: false,
                processData: false,
                contentType: false,
                enctype: 'multipart/form-data',
                success: function (response){
                
                var ruta="modificar_enfermedad".concat(response.id_enfermedad)  
                window.location.replace(ruta);
            
                },
                error: function(xhr, errmsg, err) {
                    console.log(xhr.status + ":" + xhr.responseText)
                }
            })
         
            
        })

         $(document).on('submit', '#modificarCarpetaEntrenamiento', function(e) 
        {
           
             e.preventDefault();
               formData.append('lengthEntrenamiento', filesEntrenamiento.length)
  
            formData.append('idEnfermedad',idEnfermedad)


            for (var i = 0; i < filesEntrenamiento.length; i++) 
            {
                formData.append('entrenamiento' + i, filesEntrenamiento[i])
            }


          

            formData.append('csrfmiddlewaretoken', csrftoken)

            $.ajax({
                
                type: 'POST',
                url: 'modificar_carpeta_entrenamiento',
                data: formData,
                cache: false,
                processData: false,
                contentType: false,
                enctype: 'multipart/form-data',
                success: function (response){
                
                var ruta="modificar_enfermedad".concat(response.id_enfermedad)  
                window.location.replace(ruta);
            
                },
                error: function(xhr, errmsg, err) {
                    console.log(xhr.status + ":" + xhr.responseText)
        
                }
            })
         
            
        })
                  $(document).on('submit', '#modificarCarpetaValidacion', function(e) 
        {

             e.preventDefault();


      
            for (var i = 0; i < filesValidacion.length; i++) 
            {
                formData.append('validacion' + i, filesValidacion[i])

            }


            formData.append('lengthValidacion', filesValidacion.length)
            formData.append('idEnfermedad',idEnfermedad)
            formData.append('csrfmiddlewaretoken', csrftoken)

            $.ajax({
                
                type: 'POST',
                url: 'modificar_carpeta_validacion',
                data: formData,
                cache: false,
                processData: false,
                contentType: false,
                enctype: 'multipart/form-data',
                success: function (response){
                
                var ruta="modificar_enfermedad".concat(response.id_enfermedad)  
                window.location.replace(ruta);
            
                },
                error: function(xhr, errmsg, err) {
                    console.log(xhr.status + ":" + xhr.responseText)
        
                }
            })
         
            
        })



})