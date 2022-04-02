test_data={rets};

function init(){
    d3.json(test_data).then(function(data){
    console.log(data)
        data.forEach((sample)=> {
        d3.select("#selDataset").append("option").text(sample).property("value",sample);      
     })})};      
    //var options = selectTag.selectAll('option').data(optionsData);
    //options.enter().append('option').attr('value',optionsData)
      
    
    init();