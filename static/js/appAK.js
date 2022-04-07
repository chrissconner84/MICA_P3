//const path = "./testing";

var gdata
//This is the D3 object getting brought in from the route
d3.json("./top_channels").then(function(data) {
    console.log(data);
gdata=data
    // var sum_likes = d3.sum(data, function(d) { return d.likes; });
    // var sum_dislikes = d3.sum(data, function(d) { return d.dislikes; });
    // var sum_view_count = d3.sum(data, function(d) { return d.view_count; });

    // // This is where the Plotly starts
    // var data = [{
    //     x: ["likes", "dislikes"],
    //     y: [sum_likes, sum_dislikes],
  
    //     type: "bar"
    // }];
  
    // var layout = {
    //   height: 400,
    //   width: 600
    // };
  
    // Plotly.newPlot("bar1", data, layout);
    // Plotly.newPlot("bar2", data, layout);

channel=data.map(item=>item.channeltitle)
counts=data.map(item=>item.count)
trace=[{y:channeltitle,x:counts,type:"bar", orientation:"h"}]
Plotly.newPlot("bar2", trace)
});