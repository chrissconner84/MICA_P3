
//Returns value of the option
function optionChanged(value){

  return value;
}
// Returns the array of values that match a particular key in a json object
function getValues(obj, key) {
  var objects = [];
  for (var i in obj) {
      if (!obj.hasOwnProperty(i)) continue;
      if (typeof obj[i] == 'object') {
          objects = objects.concat(getValues(obj[i], key));
      } else if (i == key) {
          objects.push(obj[i]);
      }
  }
  return objects;
}

// Random color generator. Not used for now but can be used if need be
function generateRandomColor(){
  let maxVal = 0xFFFFFF; // 16777215.
  let randomNumber = Math. random() * maxVal;
  randomNumber = Math. floor(randomNumber);
  randomNumber = randomNumber. toString(16);
  let randColor = randomNumber. padStart(6, 0);
  return `#${randColor. toUpperCase()}`
}

//Plot of View count vs Channel titles fo different category codes
d3.json("/mj").then(function(bob) {
  // Returns list of channeltitles, count and categories
  var top_channel=bob.map(function (bob1) {return bob1.channeltitle} )
  var top_count=bob.map(function (bob1) {return bob1.count} )
  var cat_codes=bob.map(function (bob1) {return bob1.cat_codes} )
  //  Retieve uniqque category codes
   unique_cat_codes = cat_codes.filter((x, i, a) => a.indexOf(x) == i)

  // Create drop down for each category code
   for (var i=0;i< unique_cat_codes.length;i++){
    // console.log("cat_codes=",cat_codes[i])
      d3.select("#selDataset1").append("option").attr("value",unique_cat_codes[i]).text(unique_cat_codes[i]);
   }

// Generate initial plot across all categories
  let trace1 = [{
      x: top_channel.slice(0,10),
      y: top_count,
      type: "bar",
      marker: {color:"blue"}
      }];
  
  //Lay Out
  var layout = {
    autosize: false,
    title: "Top Channels",
    titlefont: { size:25 },
    width: 500,
    height: 500,
    xaxis: {
          title: {
            text: 'Channel Titles'
          },
          automargin: true,
          titlefont: { size:20 },
        },
    yaxis: {
      title: 'Total Number of Days Trending',
      automargin: true,
      titlefont: { size:20 },
    },

    // paper_bgcolor: '#7f7f7f',
    // plot_bgcolor: '#c7c7c7'
  };
  // Init plot
  Plotly.newPlot("bar1", trace1, layout)
// Wait for another input sselection and call getData 
  d3.selectAll("#selDataset1").on("change", function () {
    getData(bob)});

})


// Function getData
function getData(data) {
  var dropdownMenu = d3.select("#selDataset1");
  // Assign the value of the dropdown menu option to a variable
  var dataset = dropdownMenu.property("value");
  console.log("dataset:",dataset);
  // Find the matching cat codes 
  var match = data.filter(obj => {
    return obj.cat_codes === dataset;
  });
  // Define a color table per key. Update matched data
  color_table=[{'Entertainment': 'red'}, {'Music': 'purple'}, {'People & Blogs': 'green'}, {'Gaming': 'purple'}, {'Sports': 'orange'}, 
  {'Comedy': 'blue'}, {'News & Politics': 'black'}, {'Film & Animation': 'yellow'},
   {'Science & Technology': 'lime'}, {'Autos & Vehicles': 'olive'}, 
   {'Education': 'navy'}, {'Travel & Events': 'teal'},
    {'Pets & Animals': 'aqua'}, {'Nonprofits & Activism': 'choclate'},{'Howto & Style':'darkblue'}]
  
    // Find the color value for a matchin category in the list.
    var color_code = getValues(color_table, dataset)
    var  updated_data = [{
    x: match.map(({channeltitle})=>channeltitle).slice(0,10),
    y: match.map(({count})=>count),
    type: "bar",
    marker: {color:color_code[0]}

  }];
  console.log("marker:",color_code)

  //Layout 
  var layout = {
    autosize: false,
    title: "Top Channels",
    titlefont: { size:25 },
    width: 500,
    height: 500,
    xaxis: {
          title: {
            text: 'Channel Titles'
          },
          automargin: true,
          titlefont: { size:20 },
        },
    yaxis: {
      title: 'Total Number of Days Trending',
      automargin: true,
      titlefont: { size:20 },
    },

  };

  Plotly.newPlot("bar1",  updated_data,layout);


};


//Second plot. No drop down menu

d3.json("/mj2").then(function(bob) {

  var top_count=bob.map(function (bob1) {return bob1.count} )
  var cat_codes=bob.map(function (bob1) {return bob1.cat_codes} )
  //  //Select the id 
   
  let trace1 = [{
      x: cat_codes,
      y: top_count,
      type: "bar"
    }];
    var layout = {
      autosize: false,
      title: "Top Channels by Most Trending Days",
      titlefont: { size:25 },
      width: 500,
      height: 500,
      xaxis: {
            title: {
              text: 'Categories'
            },
            automargin: true,
            titlefont: { size:20 },
          },
      yaxis: {
        title: 'Total Number of Days Trending',
        automargin: true,
        titlefont: { size:20 },
      },
    };
  
  Plotly.newPlot("bar2", trace1, layout)

})
