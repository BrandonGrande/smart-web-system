document.addEventListener('DOMContentLoaded', function() {
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

        $(document).on('submit', '#buscarEnfermedad', function(e) 
        {
            e.preventDefault();
            formData.append('nombreEnfermedad', $('#nombreEnfermedad').val())
            formData.append('tipoPatogeno', $('#tipoPatogeno').val())
            formData.append('csrfmiddlewaretoken', csrftoken)

            $.ajax({
                
                type: 'POST',
                url: 'biblioteca',
                data: formData,
                cache: false,
                processData: false,
                contentType: false,
                enctype: 'multipart/form-data',
                success: function (response){
           
           const enfermedades=response['enfermedades'];
           const resultados=response['resultados'];

           let template = '';
                enfermedades.forEach(enfermedad => {

                	  template+=`

                	  	<div class="col-md-4">
		<div class="card mb-3" style="max-width: 540px;">
  <div class="row justify-content-center">
    <div class="col-8 mt-3">
      <img src="${enfermedad.imagen}" class="card-img img-thumbnail">
    </div>
    <div class="col-12">
      <div class="card-body">
        <h5 class="card-title"><a href="consultar_enfermedad${enfermedad.id_enfermedad}"> ${enfermedad.nombre} </a> </h5>
        <p class="card-text">${enfermedad.informacion}...</p>
        <p class="card-text"><p class="text-muted">${enfermedad.tipoPatogeno}</p></p>
      </div>
    </div>
  </div>
</div>
	</div>

                     `

                });

let templateResultados=`

            
           

        <div class="col-12">
            <div class="card">
                <ul class="list-group list-group-flush">   
                <li class="list-group-item">
                        <div class="text-muted">Resultados encontrados: ${resultados}</div>
                </ul>
           </div>
   
          
                     `;


$('#contenedorEnfermedades').html(template);
$('#contenedorResultado').html(templateResultados);







              
            
                },
                error: function(xhr, errmsg, err) {
                    console.log(xhr.status + ":" + xhr.responseText)
                }
            })
         
            
        })
});