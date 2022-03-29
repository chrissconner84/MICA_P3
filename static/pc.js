function init() {
    var data = [{
        values: [5,10,25],
        labels: ["T1","T2","T3"],
      type: "pie"
    }];
  
    var layout = {
      height: 600,
      width: 800
    };
  
    Plotly.newPlot("pie", data, layout);
  };
  init();