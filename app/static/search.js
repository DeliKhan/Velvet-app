//connection between python and javascript established
var socket = io.connect('http://' + document.domain + ':' + location.port);

// Get the modal
var modal = document.getElementById('id01');

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
    const urlParams = new URLSearchParams(window.location.search);
    const myParam = urlParams.get('name');
    document.getElementById("add_item").value = myParam;
    input = document.getElementById("add_item");
    // Execute a function when the user releases a key on the keyboard
    input.addEventListener("keyup", function(event) {
    // Number 13 is the "Enter" key on the keyboard
    if (event.keyCode === 13) {
        // Cancel the default action, if needed
        event.preventDefault();
        // Trigger the button element with a click
        document.getElementById("submit_button").click();
    }
    }); 
}

//Since the user sent a query, this function will get the query string and send it too the server
socket.on('connect',function(){
    const urlParams = new URLSearchParams(window.location.search);
    var query = {};
    for(var value of urlParams.keys()) {
        if (value !== "pg"){
            query[value] = urlParams.get(value);
        }
    }
    socket.emit('searcher',query);
});

//function to create the cards for the recipes
function display(json,page_num){
    pages = Math.ceil(json.length/200);
    page_bar = document.createElement("ul");
    page_bar.setAttribute("class", "pagination justify-content-center");
    page_bar.setAttribute("style","margin:20px")
    //Make it first for the previous button
    link = document.createElement("a");
    link.setAttribute("class","page-link");
    //link.setAttribute("href",window.location.search+"&pg="+t.toString());
    link.innerText = "Previous";
    item=document.createElement("li");
    item.setAttribute("class","page-item");
    item.setAttribute("id","page");
    item.appendChild(link)
    page_bar.appendChild(item);
    for (var t=1;t<=pages;t++){
        link = document.createElement("a");
        link.setAttribute("class","page-link");
        //url = (window.location.search).split("&pg=");
        //link.setAttribute("href",url[0]+"&pg="+t.toString());
        link.innerText = t;
        item=document.createElement("li");
        item.setAttribute("class","page-item");
        item.setAttribute("id","page");
        item.appendChild(link);
        page_bar.appendChild(item);
    }
    //Make a next button at the end
    link = document.createElement("a");
    link.setAttribute("class","page-link");
    //link.setAttribute("href",window.location.search+"&pg="+t.toString());
    link.innerText = "Next";
    item=document.createElement("li");
    item.setAttribute("class","page-item");
    item.setAttribute("id","page");
    item.appendChild(link)
    page_bar.appendChild(item);
    parent = document.getElementsByClassName("col-lg-11")[0];
    parent.appendChild(page_bar);
    //query string for page number
    //const urlParams = new URLSearchParams(window.location.search);
    //page_num = parseInt(urlParams.get("pg"));
    justify_div = document.createElement("div");
    justify_div.setAttribute("class","d-flex justify-content-between");
    justify_div.setAttribute("id",0);
    if (json.length<200){
        start=0;
        end=json.length;
    }
    else{
        start=(page_num-1)*200;
        end=(page_num*200);
    }
    console.log(start);
    console.log(end);
    container = document.createElement("div");
    container.setAttribute("id","holder");
    counter = 1;
    for (var i=start;i<end;i++){
        //Extract data
        title = json[i][0];
        difficulty = json[i][1];
        rating = json[i][6];
        image = json[i][7];
        serving_size = json[i][5];
        //create elements (see sample output)
        main_div = document.createElement("div");
        main_div.setAttribute("class","card");
        main_div.setAttribute("style","width:400px;height:650px");
        img = document.createElement("img");
        img.setAttribute("class","card-img-top");
        img.setAttribute("src",image);
        img.setAttribute("alt","Card image");
        first_div = document.createElement("div");
        first_div.setAttribute("class","card-body");
        header = document.createElement("h4");
        header.setAttribute("class","card-title");
        header.innerText = title;
        difficult = document.createElement("p");
        difficult.setAttribute("class","card-text");
        difficult.setAttribute("id","difficulty");
        difficult.text = difficulty;
        stars = document.createElement("p");
        stars.setAttribute("class","card-text");
        stars.setAttribute("id","rating");
        stars.innerText = rating;
        servings = document.createElement("p");
        servings.setAttribute("class","card-text");
        servings.setAttribute("id","servings");
        servings.innerText = serving_size;
        link = document.createElement("a");
        link.setAttribute("class","btn btn-primary");
        link.setAttribute("id",i);
        //link.setAttribute("href","{{ url_for('recipe') }}");
        link.innerText = "Create Recipe!"
        first_div.appendChild(header);
        first_div.appendChild(difficult);
        first_div.appendChild(stars);
        first_div.appendChild(servings);
        first_div.appendChild(link);
        main_div.appendChild(img);
        main_div.appendChild(first_div);
        column = document.createElement("div");
        column.setAttribute("class","p-2");
        column.appendChild(main_div);
        justify_div.appendChild(column);
        //Displays three results per row
        if (counter %3 == 0){
            container.appendChild(justify_div);
            justify_div = document.createElement("div");
            justify_div.setAttribute("class","d-flex justify-content-between");
            justify_div.setAttribute("id",i);
        }
        counter += 1;
    }
    parent.appendChild(container);
}
//Sample output of what the above function prints out
/*
<div class="card" style="width:400px">
  <img class="card-img-top" src="img_avatar1.png" alt="Card image">
  <div class="card-body">
    <h4 class="card-title">John Doe</h4>
    <p class="card-text">Some example text.</p>
    <a href="#" class="btn btn-primary stretched-link">See Profile</a>
  </div>
</div>
*/

//This function will display the results from the database
socket.on('results',function(json) {
    console.log(json);
    document.getElementById("temp").value = json;
    //localStorage.setItem("temp",JSON.stringify(json));
    display(json,1);
});

//This function allows the search bar on the search page to work
$(document).on('click', '#submit_button', function() {
    var search = document.getElementById("add_item").value;
    location.href = ("/search?name=" + search);
});

//This function allows filters to be passed
$(document).on('click', '#submit', function() {
    query = {}
    var name = document.getElementById("add_item").value;
    query["name"] = name;
    var hardness = document.getElementById("hardness");
    var hardness_value = hardness.options[hardness.selectedIndex].text;
    if (hardness_value !== null){
        query["hardness"] = hardness_value;
    }
    else {
        query["hardness"] = "";
    }
    var servings = document.getElementById("serving").value;
    if (servings !== ""){
        query["servings"] = servings;
    }
    else {
        query["servings"] = "";
    }
    //to be dealt with later
    query["rating"] = "";
    var ingredients = document.getElementById("ingredients").value;
    if (ingredients !== null){
        query["ingredients"] = ingredients;
    }
    else {
        query["ingredients"] = "";
    }
    href = "/search?"
    for (name of Object.keys(query)){
        if (name == Object.keys(query)[0]){
            href += name+"="+query[name];
        }
        else{
            href += "&"+name+"="+query[name];
        }
    }
    location.href = href;
});

$(document).on('click', 'a', function() {
    if (this.getAttribute("class") == "btn btn-primary"){
        array = document.getElementById("temp").value;
        value = this.getAttribute("id");
        results = array[value];
        json = {"title":results[0],"difficulty":results[1],"time":results[2],"servings":results[5],"rating":results[6],"ingredients":results[8],"directions":results[9],"image":results[7]}
        localStorage.setItem("temp",JSON.stringify(json));
        location.href = 'http://' + document.domain + ':' + location.port + "/recipe";
    }
    else {
        
        //Data stored in a hidden div (can't do localstorage, too many values. IK, its not safe, but no easy way out
        results = document.getElementById("temp").value;
        parent = document.getElementsByClassName("col-lg-11")[0];
        child = document.getElementById("holder");
        page_bar = document.getElementsByClassName("pagination justify-content-center")[0];
        //remove all the data for the original page along with the bar with the pages
        parent.removeChild(child);
        parent.removeChild(page_bar);
        //results = JSON.parse(localStorage.getItem("temp"));
        if (this.innerText == "Previous"){
            page_num = parseInt(this.innerText)-1;
        }
        else if (this.innerText == "Next"){
            page_num = parseInt(this.innerText)+1;
        }
        else{
            page_num = parseInt(this.innerText);
        }
        //Insert new page data along with page_bar
        display(results,page_num);
    }
});
//$(document).on('click', '.', function() {
    //card = $(this).parent();
    //title = card.getELementsByTagName("h4")[0].innerText;
    //difficulty = card.getElementById("difficulty").text;
    //rating = card.getElementById("rating").innerText;
    //card_major = $(card).parent();
    //image = card_major.getELementsByTagName("img")[0].getAttribute("src");
    
//});

