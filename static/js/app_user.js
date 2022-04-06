//const path = "./testing";
//This is where the D3 gets the data from teh route
d3.json("./testing").then(function(data) {
    console.log(data);
     
     d3.sum(data, function(d) { return d.likes; }); 
     var columnsIn = data[0]; 
     for(var key in columnsIn){
       console.log(key)}; // here is your column name you are looking for
     var sum_likes = d3.sum(data, function(d) { return d.likes; });
     var sum_dislikes = d3.sum(data, function(d) { return d.dislikes; });

// This is where the Plotly starts    

    var data = [{
        x: columnsIn,
        y: [sum_likes, sum_dislikes],
  
        type: "bar"
    }];
  
    var layout = {
      height: 400,
      width: 400
    };
  
    
    Plotly.newPlot("bar4", data, layout);
    Plotly.newPlot("bar5", data, layout);
    Plotly.newPlot("bar6", data, layout);
});

d3.json("./country").then(function(data_country) {
  //console.log(data_country);
  countries=[]
  vc_list=[]
  lr_list=[]
  cc_list=[]
  es_list=[]
   for (var i = 0; i < data_country.length; i++) {
    var countryname = data_country[i].country;
    countries.push(countryname)
     var vc = data_country[i].view_count;
     vc_list.push(vc)
     var lr = data_country[i].likes_ratio;
     lr_list.push(lr)
     var cc = data_country[i].comment_count;
     cc_list.push(cc)
     var es = data_country[i].engagement_score;
     es_list.push(es)
  
  }
  
  var cht=document.getElementById("bar3").getContext("2d")
  var barChart=new Chart(cht,{
    type:'bar',
    data:{
      labels: countries,
      datasets:[
        {
        label:"Countries View Counts",
        data: vc_list,
        fill:false,
        bordercolor:"rgb (75,192,192)",
        lineTension: 0.1, 
    }]},
      options: {
      responsive:false
    }
  })
  var cht=document.getElementById("bar4").getContext("2d")
  var barChart=new Chart(cht,{
    type:'bar',
    data:{
      labels: countries,
      datasets:[
        {
        label:"Countries Likes Ratio",
        data: vc_list,
        fill:false,
        bordercolor:"rgb (75,192,192)",
        lineTension: 0.1, 
    }]},
      options: {
      responsive:false
    }
  })

  var cht=document.getElementById("bar5").getContext("2d")
  var barChart=new Chart(cht,{
    type:'bar',
    data:{
      labels: countries,
      datasets:[
        {
        label:"Countries Comments Count",
        data: cc_list,
        fill:false,
        bordercolor:"rgb (75,192,192)",
        lineTension: 0.1, 
    }]},
      options: {
      responsive:false
      }
})  

var cht=document.getElementById("bar6").getContext("2d")
  var barChart=new Chart(cht,{
    type:'bar',
    data:{
      labels: countries,
      datasets:[
        {
        label:"Engagement Score Count",
        data: es_list,
        fill:false,
        bordercolor:"rgb (75,192,192)",
        lineTension: 0.1, 
    }]},
      options: {
      responsive:false
      }
})  
});
  
