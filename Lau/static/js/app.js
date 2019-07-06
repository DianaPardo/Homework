function init(){
    console.log('hello world 4')
    //agregar a la lista de equipos
    var selector = d3.select('#myMenu');
    d3.json("/names").then((club) => {
        selector.selectAll("li")
        .data(club)
        .enter()
        .append("li")
        .html(function(d) {
            return `<li><a href="" onclick="equipo(this.text);return false;">${d.club}</a></li>`;
        });
    });
};

init();

//formating
// function format(string){
//     var s = String(string).replace(/(.)(?=(\d{3})+$)/g,'$1,');
//     return s;
// };

var format = function(n, dp){
    var e = '', s = e+n, l = s.length, b = n < 0 ? 1 : 0,
        i = s.lastIndexOf('.'), j = i == -1 ? l : i,
        r = e, d = s.substr(j+1, dp);
    while ( (j-=3) > b ) { r = ',' + s.substr(j, 3) + r; }
    return s.substr(0, j + 3) + r + 
      (dp ? '.' + d + ( d.length < dp ? 
          ('00000').substr(0, dp - d.length):e):e);
};

// función para buscar en la lista de equipos
function myFunction() {
    var input, filter, ul, li, a, i;
    input = document.getElementById("mySearch");
    filter = input.value.toUpperCase();
    ul = document.getElementById("myMenu");
    li = ul.getElementsByTagName("li");
    for (i = 0; i < li.length; i++) {
        a = li[i].getElementsByTagName("a")[0];
        if (a.innerHTML.toUpperCase().indexOf(filter) > -1) {
        li[i].style.display = "";
        } else {
        li[i].style.display = "none";
        }
    }
};

function mean(arr) {
    var total = 0;
    for (var i = 0; i < arr.length; i++) {
      total += arr[i];
    }
    var meanValue = total / arr.length;
  
    return meanValue;
};

var max_w; //declarar como variable global el valor máximo

function equipo(value){
    //llenar la lista de jugadores
    var selector = d3.select('#playerslist');
    selector.html("");
    var Uteam = value.toUpperCase();
    d3.select('#team').text(Uteam);
    d3.json(`/names/${value}`).then((players) => {
        //crear arrays
        var aggression = players.map(function(d){
            return d.aggression;
        });
        var overall = players.map(function(d){
            return d.overall;
        });
        var wage = players.map(function(d){
            return d.wage;
        });
        var aggression_mean = mean(aggression);
        var overall_mean = mean(overall);
        var wage_mean = mean(wage);
        // player_value máximo
        max_w = Math.max.apply(null,wage);
        console.log(`nuevo máximo: ${max_w}`)       
        d3.select("#team-yellow").text(format(wage_mean));
        d3.select("#team-red").text(format(aggression_mean));
        d3.select("#team-green").text(format(overall_mean));
        selector.selectAll("a")
        .data(players)
        .enter()
        .append("a")
        .html(function(d) {
            return `<a class="dropdown-item" href="" onclick="player(this.text);return false;">${d.player_name}</a>`;
        });
    });//termina promesa
};

function player(value){
    d3.json(`/names/player/${value}`).then((players) => {
    var p_overall = players.overall[0];
    var p_wage = players.wage[0];
    var p_aggression = players.aggression[0];
    var n_nationality = players.nationality[0];
    d3.select('#player_name').text(value);
    d3.select('#nationality').text(n_nationality);
    //scalar
    var w_overall = p_overall * 3.6;
    var w_wage = p_wage * (360/max_w);//cambiar
    var w_aggression = p_aggression * 3.6;
    //modificar width y testo
    d3.select("#rect-red").attr("width",w_aggression);
    d3.select("#rect-green").attr("width",w_overall);
    d3.select("#rect-yellow").attr("width",w_wage);
    d3.select("#player_yellow").text(format(p_wage));
    d3.select("#player_red").text(p_aggression);
    d3.select("#player_green").text(p_overall);
});
};
