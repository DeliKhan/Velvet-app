google.charts.load('current', {
  'packages': ['corechart']
});
google.charts.setOnLoadCallback(drawChart);

var socket = io.connect('http://' + document.domain + ':' + location.port);
socket.on('connect', function(msg) {
    socket.emit('fridge_info', "connected");
    console.log("hi");
});
socket.on('message', function(msg){
    console.log(msg);
    console.log("connected");
});
  
function drawChart() {

  var data = google.visualization.arrayToDataTable([
    ['Food Group', 'Serving'],
    ['Meats and Alternatives', 11],
    ['Grains', 2],
    ['Vegetables', 2],
    ['Milk and Alternatives', 2],
  ]);

  var options = {
    title: 'My Daily Activities',
    backgroundColor: "none",
    titleTextStyle: {color: "white"},
    pieSliceBorderColor: "none",
    legend:{textStyle:{color: "white"}},
};

  var chart = new google.visualization.PieChart(document.getElementById('piechart'));

  chart.draw(data, options);

}
