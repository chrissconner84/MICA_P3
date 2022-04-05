//const path = "./testing";

// Promise Pending
// const dataPromise = d3.json(path);
// console.log("Data Promise: ", dataPromise);


// // Fetch the JSON data and console log it
// d3.json(path).then(function(data) {
// console.log(data);
// d3.selectAll("#selDataset").on("change", getData);
// });
// // Function called by DOM changes
// function getData() {
// //var optionsData = data.names;
// //console.log(optionsData)
// //var selectTag = d3.select("#selDataset")
// data.items.id.forEach((category)=> {
// d3.select("#selDataset").append("option").text(category).property("value",category);
// })
// };

d3.json("./testing").then(function(data) {
    console.log(data);

     var sum_likes = d3.sum(data, function(d) { return d.likes; });
     var sum_dislikes = d3.sum(data, function(d) { return d.dislikes; });
    // var sum_view_count = d3.sum(data, function(d) { return d.view_count; });

    var data = [{
        x: ["likes", "dislikes"],
        y: [sum_likes, sum_dislikes],
  
        type: "bar"
    }];
  
    var layout = {
      height: 400,
      width: 400
    };
  
    //Plotly.newPlot("bar3", data, layout);
    Plotly.newPlot("bar4", data, layout);
    Plotly.newPlot("bar5", data, layout);
    Plotly.newPlot("bar6", data, layout);
});

d3.json("./country").then(function(data_country) {
  console.log(data_country);
  // data_country.forEach(function(data) {
  //  var cols=Object.values(data[0])
  //  console.log(cols)
  vc_list=[]
   for (var i = 0; i < data_country.length; i++) {
    var vc = data_country[i].view_count;
    vc_list.push(vc)
    // var lr = data_country[i].view_count;
    // var cc = data_country[i].view_count;
    // var es = data_country[i].view_count;
  
  }
  console.log(vc_list)
});
  
  //  var countries=d3.values(data_country, function(d) { return d.country; });
  //  var vc = d3.values(data_country, function(d) { return d.view_count; });
  //  var lr = d3.values(data_country, function(d) { return d.likes_ratio; });
  //  var cc = d3.values(data_country, function(d) { return d.comment_count; });
  //  var es = d3.values(data_country, function(d) { return d.engagement_score; });
//   var data = [{
//       x: ['View Count'],
//       y:[vc],

//       type: "bar"
//   }];

//   var layout = {
//     height: 400,
//     width: 400
//   };

//   Plotly.newPlot("bar3", data, layout);

// function init() {
//     var data = [{
//         values: [5,10,25],
//         labels: ["T1","T2","T3"],
//       type: "pie"
//     }];
  
//     var layout = {
//       height: 600,
//       width: 800
//     };
  
//     Plotly.newPlot("pie", data, layout);
//   };
//   init();
// function init(){
// d3.json(path).then(function(data){
//     var categories=data.items;
//     //console.log(categories)
//     for (var i=0; i < categories.length;i++){
//         var cat_id=((categories)[i].id)
//         //cat_id.forEach((category)=> {
//         d3.select("#selDataset").append("option").text(cat_id).property("value",cat_id);
      
//var options = selectTag.selectAll('option').data(optionsData);
//options.enter().append('option').attr('value',optionsData)

