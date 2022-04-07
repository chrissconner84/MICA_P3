var map = L.map('map').setView([52.52, 13.40], 2);


L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    maxZoom:18
 }).addTo(map);

 // Creating a new marker:
 // create array of countries:
//  var countries=['United States','Great Britain','Mexico','Russia','Japan','South Korea','Canada','France','Germany','India','Brazil']
//  var cap_lat=[38.90,51.50,19.43,55.75,35.67,37.56,45.42,48.85,52.52,19.07,-22.90]
//  var cap_lon=[-77.03, 0.12,-99.13,37.61,139.65,126.97,-75.69,2.35,13.40,72.87,-43.17]
//  var cap_markers=[]
// // We pass in some initial options, and then add the marker to the map by using the addTo() method.
// for (var index = 0; index < countries.length; index++) {
//     var marker = L.marker([cap_lat[index],cap_lon[index]])
//     .addTo(map)
//     marker.bindPopup(countries[index])

// };
// Store our API endpoint as queryUrl.
// NOT NEEDED var queryUrl = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2021-01-01&endtime=2021-01-02&maxlongitude=-69.52148437&minlongitude=-123.83789062&maxlatitude=48.74894534&minlatitude=25.16517337";
//"Country"=countries[index],"Total Days"=
// Perform a GET request to the query URL/
d3.json("/wm_fill").then(function (data) {
  // Once we get a response, send the data.features object to the createFeatures function.
  
  var countries=data.map(function (country_get) {return country_get.country_name} )
  var lat=data.map(function (lat_get) {return lat_get.cap_lat} )
  var lon=data.map(function (lon_get) {return lon_get.cap_lon} )
  var total_records=data.map(function (records_get) {return records_get.total_days} )
  console.log('all data:',data,"my countries:",countries,
  "capital lat:",lat,"capitla lon:",lon,"total days:",total_records)

  for (var index = 0; index < countries.length; index++) {
    var test=countries[index]+" has "+total_records[index] +" videos in our dataset"
    var zlat=lat[index]
    var zlon=lon[index]
    //var latlng=(zlat,zlon)
    var marker = L.marker([lat[index],lon[index]])
    
    .addTo(map)
    marker.bindPopup(test)
    marker.on('click', function(e){
        map.setView(e.latlng, 5);
    });
     marker.on('mouseout', function(e){
         map.setView([52.52, 13.40], 2);
     });



  //createFeatures(data.features);

  }});

function createFeatures(earthquakeData) {

  // Define a function that we want to run once for each feature in the features array.
  // Give each feature a popup that describes the place and time of the earthquake.
  function onEachFeature(feature, layer) {
    layer.bindPopup(`<h3>${feature.properties.place}</h3><hr><p>${new Date(feature.properties.time)}</p>`);
  }

  // Create a GeoJSON layer that contains the features array on the earthquakeData object.
  // Run the onEachFeature function once for each piece of data in the array.
  var earthquakes = L.geoJSON(earthquakeData, {
    onEachFeature: onEachFeature
  });

  // Send our earthquakes layer to the createMap function/
  createMap(earthquakes);
}

function createMap(earthquakes) {

  // Create the base layers.
  var street = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
  })

  var topo = L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
    attribution: 'Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)'
  });

  // Create a baseMaps object.
  var baseMaps = {
    "Street Map": street,
    "Topographic Map": topo
  };

  // Create an overlay object to hold our overlay.
  var overlayMaps = {
    Earthquakes: earthquakes
  };

  // Create our map, giving it the streetmap and earthquakes layers to display on load.
  var myMap = L.map("map", {
    center: [
      37.09, -95.71
    ],
    zoom: 5,
    layers: [street, earthquakes]
  });

  // Create a layer control.
  // Pass it our baseMaps and overlayMaps.
  // Add the layer control to the map.
  L.control.layers(baseMaps, overlayMaps, {
    collapsed: false
  }).addTo(myMap);

}


    

  
  
  