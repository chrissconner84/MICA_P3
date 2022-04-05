//const path = "./testing";


//This is the D3 object getting brought in from the route
d3.json("./testing").then(function(data) {
    console.log(data);

    var sum_likes = d3.sum(data, function(d) { return d.likes; });
    var sum_dislikes = d3.sum(data, function(d) { return d.dislikes; });
    var sum_view_count = d3.sum(data, function(d) { return d.view_count; });

    // This is where the Plotly starts
    var data = [{
        x: ["likes", "dislikes"],
        y: [sum_likes, sum_dislikes],
  
        type: "bar"
    }];
  
    var layout = {
      height: 400,
      width: 600
    };
  
    Plotly.newPlot("bar1", data, layout);
    Plotly.newPlot("bar2", data, layout);
});


