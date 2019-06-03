window.onload=function(){
    info = JSON.parse(localStorage.getItem("temp"));
    document.getElementsByTagName("h4")[0].innerText = info["title"];
    document.getElementById("difficulty").innerText = "Difficulty: " + info["difficulty"];
    document.getElementById("time").innerText = "Total time: " + info["time"];
    document.getElementById("servings").innerText = "Serving Size: " + info["servings"];
    rating = parseInt(info["rating"][0]);
    rate = document.getElementById("rating_div");
    for (var i = 1; i<= 5; i++){
        span = document.createElement("span");
        if (i < rating){
            span.setAttribute("class","fa fa-star checked");
        }
        else {
            span.setAttribute("class","fa fa-star");
        }
        rate.appendChild(span);
    }
    ingredients = info["ingredients"];
    list = ingredients.split("?!?@");
    parent = document.getElementById("ingredients");
    for (var t=0;t<list.length;t++){
        ingredient = document.createElement("li");
        ingredient.setAttribute("class","list-group-item");
        ingredient.innerText = list[t];
        parent.appendChild(ingredient);
    }
    document.getElementsByTagName("img")[1].setAttribute("src",info["image"]);
    directions = info["directions"];
    new_directions = directions.replace("?!?@",".");
    steps = new_directions.split(".");
    parent = document.getElementById("directions");
    for (var t=0;t<steps.length;t++){
        step = document.createElement("li");
        step.setAttribute("class","list-group-item");
        step.innerText = steps[t];
        parent.appendChild(step);
    }
}
    
                
