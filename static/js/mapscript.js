var map = L.map('map').setView([52.52, 13.40], 2);


L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    maxZoom:18
 }).addTo(map);

 // Creating a new marker:
 // create array of countries:
 var countries=['United States','Great Britain','Mexico','Russia','Japan','South Korea','Canada','France','Germany','India','Brazil']
 var cap_lat=[38.90,51.50,19.43,55.75,35.67,37.56,45.42,48.85,52.52,19.07,-22.90]
 var cap_lon=[-77.03, 0.12,-99.13,37.61,139.65,126.97,-75.69,2.35,13.40,72.87,-43.17]
 var cap_markers=[]
// We pass in some initial options, and then add the marker to the map by using the addTo() method.
for (var index = 0; index < countries.length; index++) {
    var marker = L.marker([cap_lat[index],cap_lon[index]])
    .addTo(map)
    marker.bindPopup(countries[index])

};

    

  
  
  