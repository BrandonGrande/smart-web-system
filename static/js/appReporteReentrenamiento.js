Highcharts.chart('container', {

    title: {
        text: 'Comportamiento de metricas durante el entrenamiento'
    },

    yAxis: {
        title: {
            text: 'Valores'
        }
    },

    xAxis: {
        title: {
            text: 'Epocas'
        }
    },

   legend: {
        layout: 'vertical',
        align: 'right',
        verticalAlign: 'middle'
    },

    plotOptions: {
        series: {
            label: {
                connectorAllowed: false
            },
            pointStart: 1
        }
    },

    series: [{
        name: 'Error',
         color: '#FF0000',
        data: errores
    },
    {
        name: 'Calidad',
        color:'#058DC7',
        data: calidad
    }


    ],
credits: {
    enabled: false
},
    responsive: {
        rules: [{
            condition: {
                maxWidth: 500
            },
          
        }]
    }

});