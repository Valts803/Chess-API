function ajaxGetRequest(path, callback){
  var request = new XMLHttpRequest();
  request.onreadystatechange = function(){
    if (this.readyState===4&&this.status ===200){
      callback(this.response);
    }
  };
  request.open("GET", path);
  request.send();
}

function ajaxPostRequest(path, data, callback){
  var request = new XMLHttpRequest();
  request.onreadystatechange = function(){
    if (this.readyState===4&&this.status ===200){
      callback(this.response);
    }
  };
  request.open("POST", path);
  request.send(data);
}

function update_elo(response) {

  var json_data = JSON.parse(response);
    //console.log(json_data['rating'])
    //console.log(json_data['no.'])
  var data = [{
    x: json_data['no.'],
    y: json_data['rating'],
    type: 'scatter'
  }];
  var layout = {
  title: 'Blitz Rating based on number of games',
  font:{family: 'Raleway, sans-serif'},
  xaxis: {title: 'Number of games'},
  yaxis: {title: 'Blitz rating'},
};


Plotly.newPlot('line', data, layout);

}

function update_countries(response) {

  var json_data = JSON.parse(response);
    //console.log(json_data[0])
    //console.log(json_data[1])

  var data = [{
    x: json_data[0],
    y: json_data[1],
    type: 'bar'
  }];
  var layout = {
  title: 'Winrate for games played against people of different nations',
  font:{family: 'Raleway, sans-serif'},
  xaxis: {title: 'Countries'},
  yaxis: {title: 'Win rate (%)'},
};

var textObj = document.getElementById("total_games");
//console.log(json_data[2]);
textObj.innerHTML = "Number of games analyzed:"
textObj.innerHTML += json_data[2].toString();

Plotly.newPlot('bar', data, layout);

var textObj = document.getElementById("loading");
textObj.innerHTML = "Done";

}


function load_page() 
{
  //ajaxGetRequest("/get_elo", update_elo);

  //ajaxGetRequest("/get_countries", update_countries);
}


function get_stats()
{

    var textObj = document.getElementById("loading");
    textObj.innerHTML = "Processing...";

    var textObj = document.getElementById("player");
    var player = textObj.value;
    textObj.value = "";


    //console.log(player);

    var data = JSON.stringify(player);

    
    ajaxPostRequest("/update_elo", data, update_elo);
    ajaxPostRequest("/update_nationalities", data, update_countries);
}
