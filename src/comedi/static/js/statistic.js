  function drawMyChart_old(getDataUrl, canvasId, charTitle, charType){
    var data = [];
    var title = [];
    if(!!document.createElement('canvas').getContext){ //check that the canvas
                                                       // element is supported
                                                       
      $.getJSON(getDataUrl,  function(titleAndData) {
          var dataPlot = titleAndData[1];
          var titlePlot = titleAndData[0];
  
                     
       var mychart = new AwesomeChart(canvasId);
       mychart.title = charTitle;
       mychart.data = dataPlot;
       mychart.labels = titlePlot;
       mychart.chartType=charType;
       mychart.randomColors = true;
       mychart.draw();
       });
       
    }
  }
  
  
  
  /*
  
Chart type  chartType property value
Horizontal bar chart    default
Vertical bar chart  horizontal bars
Pareto chart    pareto
Pie chart   pie
Exploded chart  exploded pie
Doughnut chart  doughnut

*/
  
  function drawMyChart(labels, data, canvasId, charTitle, charType){

    if(!!document.createElement('canvas').getContext){ //check that the canvas
                                                       // element is supported
       $( ".canvas_holder").append( '<canvas id="' + canvasId+ '" width="500" height="500">Your web-browser does not support the HTML 5 canvas element.</canvas>' );
                    
       var myCanvas = document.getElementById(canvasId);                                  
       myCanvas.width = myCanvas.width;                                 
       var mychart = new AwesomeChart(canvasId);
       mychart.title = charTitle;
       mychart.data = data;
       mychart.labels = labels;
       mychart.chartType=charType;
       mychart.randomColors = true;
       mychart.draw();
       
       
    }
  }