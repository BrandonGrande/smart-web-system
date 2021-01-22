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
        formData.append('id_diagnostico', id_diagnostico)
             formData.append('csrfmiddlewaretoken', csrftoken)
        $.ajax({
                
                type: 'POST',
                url: 'cargar_grafico',
                data: formData,
                cache: false,
                processData: false,
                contentType: false,
                enctype: 'multipart/form-data',
                success: function (response){
                console.log(response);
                cargarGrafica(response);
    
                },
                error: function(xhr, errmsg, err) {
                    console.log(xhr.status + ":" + xhr.responseText)
                }
            })


function cargarGrafica(valores){
Highcharts.chart('container', {
    chart: {
        plotBackgroundColor: null,
        plotBorderWidth: null,
        plotShadow: false,
        type: 'pie'
    },
    title: {
        text: 'Porcentajes de enfermedades en el cultivo'
    },
    tooltip: {
        pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
    },
    accessibility: {
        point: {
            valueSuffix: '%'
        }
    },
    plotOptions: {
        pie: {
            allowPointSelect: true,
            cursor: 'pointer',
            dataLabels: {
                enabled: true,
                format: '<b>{point.name}</b>: {point.percentage:.1f} %'
            }
        }
    },
credits: {
    enabled: false
},
    series: [

    {
        name: 'Porcentaje',
        colorByPoint: true,
        data: valores
    }

    ]
});

}

});