var chart = null;

var CHART_ACTUAL_DEPTH = 0;
var CHART_PLAN_DEPTH = 1;
var CHART_DWOP = 2;
var CHART_ACTUAL_COST = 3;
var CHART_PLAN_COST = 4;

function init_dual_axis(canvas){

Chart.defaults.global.defaultFontFamily = "Lato";
Chart.defaults.global.defaultFontSize = 18;
Chart.defaults.global.elements.point.radius = 0;
Chart.defaults.global.elements.point.hitRadius = 20
Chart.defaults.global.elements.point.hoverBorderWidth = 4;


var canvas = document.getElementById(canvas);

chart = new Chart(canvas, {
  type: 'line',

  data: {
    datasets: [{
      label: 'Actual Depth',
      yAxisID: 'A',
      borderColor: 'red',
data: [
  { x: 19, y: -65 }, { x: 27, y: -59 }, { x: 28, y: -69 }, { x: 40, y: -81 },
  { x: 48, y: -56 }, { x: 86, y: -55 }, { x: 90, y: -40 }, { x: 95, y: -60 }
], fill:false
    }, {
      label: 'Plan Depth',
      yAxisID: 'A',

      data: [],
borderColor: 'blue',
fill:false
    }, {
      label: 'DWOP',
      yAxisID: 'A',
      data: [],
borderColor: 'orange',
fill:false
    }, {
      label: 'Actual Cost',
      yAxisID: 'B',
      data: [],
borderColor: 'red',

fill:false
    }, {
      label: 'Plan Cost',
      yAxisID: 'B',
      data: [],
borderColor: 'blue',

fill:false
    }



  ] //--end of datasets
}, //-- end of chart data
  options: {
    scales: {
      xAxes: [{
    type: 'linear',
    position: 'top' ,
    display: true,
    labelString: 'Days'}],
      yAxes: [{
        id: 'A',
        type: 'linear',
        position: 'left',
        display: true,
        labelString: 'Depth (meters)'
      }, {
        id: 'B',
        type: 'linear',
        position: 'right',
        beginAtZero:true,
        display: true,
        labelString: 'Cost (Php)'
      }]
    }
  }
});

}

function change_chart_data(index, data){
  console.log('changing chart data');

  var points = [];

// if related to depth, multiply by -1
  if (index < 3) {
  data.forEach(function(point){
      points.push({x: point[0], y: -1 * point[1]});
    }); }

  else{
    data.forEach(function(point){
        points.push({x:point[0], y:point[1]/Math.pow(10,6)});
      });
  }

  chart.data.datasets[index].data = points;

  chart.update();


}

function get_chart_data(index){

  return chart.data.datasets[index].data;
}
