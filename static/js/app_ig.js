const path = "./Resources/US_category_id.json";

// Promise Pending
const dataPromise = d3.json(path);
console.log("Data Promise: ", dataPromise);

// var df = '{{df}}'
// console.log(df)
// // Fetch the JSON data and console log it
d3.json(path).then(function(data) {
//console.log(data);
d3.selectAll("#selDataset").on("change", getData);
});
// Function called by DOM changes
function getData() {
//var optionsData = data.names;
//console.log(optionsData)
//var selectTag = d3.select("#selDataset")
data.items.id.forEach((category)=> {
d3.select("#selDataset").append("option").text(category).property("value",category);
})};

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

