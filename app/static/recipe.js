//Objective: When window loads up, get data on what recipe the person clicked on (via localstorage), and then display it in a user-friendly way
window.onload=function(){
    info = JSON.parse(localStorage.getItem("temp"));
    document.getElementsByTagName("h4")[0].innerText = info["title"];
    document.getElementById("difficulty").innerText = "Difficulty: " + info["difficulty"];
    document.getElementById("time").innerText = "Total time: " + info["time"];
    document.getElementById("servings").innerText = "Serving Size: " + info["servings"];
    rating = parseInt(info["rating"][0]);
    rate = document.getElementById("rating_div");
    //This is unique, cause instead of text, we want to put stars. So, the function below looks at the amount of stars given and makes that many stars
    for (var i = 1; i<= 5; i++){
        span = document.createElement("span");
        if (i < rating){
            //checked means it shows up as a golden star
            span.setAttribute("class","fa fa-star checked");
        }
        else {
            //shows up as a blank star
            span.setAttribute("class","fa fa-star");
        }
        rate.appendChild(span);
    }
    ingredients = info["ingredients"];
    list = ingredients.split("?!?@");
    parent = document.getElementById("ingredients");
    //I'm basically making a list with each element being each ingredient
    for (var t=0;t<list.length;t++){
        ingredient = document.createElement("li");
        ingredient.setAttribute("class","list-group-item");
        ingredient.innerText = list[t];
        parent.appendChild(ingredient);
    }
    document.getElementsByTagName("img")[1].setAttribute("src",info["image"]);
    directions = info["directions"];
    //Yea, weird thing. Deluckshan's code uses the period and this random bit to seperate each step. So first make it all into periods
    new_directions = directions.replace("?!?@",".");
    //now split by periods
    steps = new_directions.split(".");
    parent = document.getElementById("directions");
    //Do same thing as with the ingredients
    for (var t=0;t<steps.length;t++){
        step = document.createElement("li");
        step.setAttribute("class","list-group-item");
        step.innerText = steps[t];
        parent.appendChild(step);
    }
}
    
                
