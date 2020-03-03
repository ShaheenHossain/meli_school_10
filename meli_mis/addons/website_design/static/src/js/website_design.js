odoo.define('website_design.website', function (require) {
    "use strict";
//    var website = require('website.website');
    var core = require('web.core');
    var Model = require("web.Model");
    var QWeb = core.qweb;

    $(document).on('click', '#sidebarCollapse', function (e) {
        $('#sidebar').toggleClass('active');
    });
    function load_pie_chart(){
        google.charts.load('current', {'packages':['corechart']});
        google.charts.setOnLoadCallback(drawChart);
        function drawChart() {
          var data = google.visualization.arrayToDataTable([
          ['Attendance Type', 'Attendance'],
          ['Present', 50],
          ['Absent', 33.5],
          ['Leaves', 2],
        ]);

          // Optional; add a title and set the width and height of the chart
          var options = {'width':550, 'height':400, legend: { position: 'bottom'}};

          // Display the chart inside the <div> element with id="piechart"
          var chart = new google.visualization.PieChart(document.getElementById('piechart'));
          chart.draw(data, options);
        }
    }
    $(document).ready(function(){
        load_pie_chart()
        $('.datepicker').datepicker();
    });

});