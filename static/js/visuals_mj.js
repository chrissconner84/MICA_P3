var all_data; 

// d3.json('/api/all_data').then(resp=>{
//     all_data = resp['response']
//      var dropdown = d3.select('#userSel')
//       d3.json('/api/country').then(country_response =>{
//           country_response['response'].forEach(element => {
//             //   dropdown.append('option').property('value', element).text(element)
//         console.log('all_data')  
//         });
//      })
//   });

// FOR THE DROP DOWN
d3.json("/api/country").then(test_data => {
    console.log(test_data);
    
    var dropdown = d3.select('#userSel');

    test_data.response.forEach(countryName => {
        dropdown.append("option").property("value", countryName).text(countryName);
    });
})

// 
d3.json("/api/cat_codes_likes_agg").then(view_data => {
    var likesList = view_data.response.map(cat_codes => cat_codes.likes)

    console.log(likesList);
})