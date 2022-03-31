var all_data; 

d3.json('/api/all_data').then(resp=>{
    all_data = resp['response']
    var dropdown = d3.select('#userSel')
    d3.json('/api/country').then(country_response =>{
        country_response['response'].forEach(element => {
            dropdown.append('option').property('value', element).text(element)
        });
    })
})
