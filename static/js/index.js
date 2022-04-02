const Client =require('pg').Client
//This is another way to write line 1
// const {Client}=require('pg')
const client=new Client({
    user:"postgres",
    password:"postgres",
    host:"http://youtube.cb1bticre0py.us-east-1.rds.amazonaws.com",
    port: 5432,
    database:"Youtube P3"
})

client.connect()
.then(()=>console.log("Connected Successfully"))
.then(()=>client.query("select * from us_data limit 3"))
.then(results =>console.table(results.rows))
.catch(e =console.log(e))
.finally(()=> client.end());

