//const path = "./testing";
var gdata

//This is the D3 object getting brought in from the route
// d3.json("./testing").then(function(data) {
//     console.log(data);
//     Object.entries(data).forEach((entry) => {
//       const [key, value] = entry;
//       console.log(`${key}: ${value}`);
//     var columnsIn = data[0]; 
//     var thekeys=[]
//     //console.log(columnsIn)
//     for(var key1 in columnsIn){
//       thekeys.push(key)
//       console.log(key1)};
//       console.log(thekeys) // here is your column name you are looking for
//     var sum_likes = d3.sum(data, function(d) { return d.likes; });
//     var sum_dislikes = d3.sum(data, function(d) { return d.dislikes; });
//     var sum_view_count = d3.sum(data, function(d) { return d.view_count; });

//     // This is where the Plotly starts
//     var data = [{
//         x: [1,2,3,4],
//         // y: [sum_likes, sum_dislikes],
//         y:[thekeys],
  
//         type: "bar"
//     }];
  
//     var layout = {
//       height: 400,
//       width: 600
//     };
  
//     Plotly.newPlot("bar1", data, layout);
//     Plotly.newPlot("bar2", data, layout);
// });

// })
d3.json("/top_channels").then(function(data) {
  //for (var i = 0; i < data.length; i++) {
    //console.log(data[i].country)
    //but need to filter by country ALSO
    //var top10 = data.sort(function(a, b) { return a.count < b.count ? 1 : -1; })
    //            .slice(0, 11);
    gdata=data
    console.log(gdata)
    // WE NEED TO FILTER FOR EACH COUNTRY, SORT BY COUNT COLUMN, SLICE TOP 10
   
    // Object.values(data).forEach((sample)=> {
    //   var top10 = sample.sort(function(a, b) { return a.count < b.count ? 1 : -1; })
    //             .slice(0, 10);
    
    // console.log(top10)            
    }
    
  //console.log(data);
    
    );

  // countries=[]
  // vc_list=[]
  // lr_list=[]
  // cc_list=[]
  // es_list=[]
  //  for (var i = 0; i < data_country.length; i++) {
  //   var countryname = data_country[i].country;
  //   countries.push(countryname)
  //    var vc = data_country[i].view_count;
  //    vc_list.push(vc)
  //    var lr = data_country[i].likes_ratio;
  //    lr_list.push(lr)
  //    var cc = data_country[i].comment_count;
  //    cc_list.push(cc)
  //    var es = data_country[i].engagement_score;
  //    es_list.push(es)
  
  // }
  
  // var cht=document.getElementById("bar3").getContext("2d")
  // var barChart=new Chart(cht,{
  //   type:'bar',
  //   data:{
  //     labels: countries,
  //     datasets:[
  //       {
  //       label:"Countries View Counts",
  //       data: vc_list,
  //       fill:false,
  //       bordercolor:"rgb (75,192,192)",
  //       lineTension: 0.1, 
  //   }]},
  //     options: {
  //     responsive:false
  //   }
  // })
// })  
d3.json("/mj").then(function(bob) {
  var top_channel=bob.map(function (bob1) {return bob1.channeltitle} )
  var top_count=bob.map(function (bob1) {return bob1.count} )
  var cat_codes=bob.map(function (bob1) {return bob1.cat_codes} )
  console.log("top_channel=",top_channel)
  console.log("top_count=",top_count)
  console.log("max=",d3.max(top_count))


  let trace1 = [{
      x: top_channel.slice(0,100),
      y: top_count,
      marker:cat_codes,
      type: "bar"
    }];
  let layout = {
    width:600,
    height:400,
    title: "Top Channels",
    barmode:"group"
    };
  
  Plotly.newPlot("bar1", trace1, layout)
})