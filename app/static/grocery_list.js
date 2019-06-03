//connection between python and javascript established
var socket = io.connect('http://' + document.domain + ':' + location.port);
//get username from localstorage to use as a unique id so that the server knows who is who
var username = localStorage.getItem("username");
//will create a row for each item on the grocery list shown in the comment below the function
function create(msg){
    //msg will look like this [["kale",1],["spinich",2]]
    for (var i=0;i<msg.length;i++){
        //names are self-explanitory, but in this part, i create each element with attributes
        main_div = document.createElement("div");
        main_div.setAttribute("class","d-flex justify-content-center");
        second_div = document.createElement("div");
        second_div.setAttribute("class","p-2");
        third_div = document.createElement("div");
        third_div.setAttribute("class","p-2");
        fourth_div = document.createElement("div");
        fourth_div.setAttribute("class","p-2");
        fifth_div = document.createElement("div");
        fifth_div.setAttribute("class","p-2");
        sixth_div = document.createElement("div");
        sixth_div.setAttribute("class","p-2");
        second_input = document.createElement("input");
        second_input.setAttribute("type","text");
        second_input.setAttribute("class","form-control");
        second_input.setAttribute("readonly","readonly");
        second_input.setAttribute("value",msg[i][0]);
        fourth_input = document.createElement("input");
        fourth_input.setAttribute("type","text");
        fourth_input.setAttribute("class","form-control");
        fourth_input.setAttribute("id",i.toString());
        fourth_input.setAttribute("readonly","readonly");
        fourth_input.setAttribute("value",msg[i][1]);
        third_button = document.createElement("button");
        third_button.setAttribute("id","down_button");
        third_button.setAttribute("class",i.toString());
        third_image = document.createElement("img");
        third_image.setAttribute("id","down");
        third_image.setAttribute("class",i.toString());
        third_image.setAttribute("src","../static/down_arrow.svg");
        fifth_button = document.createElement("button");
        fifth_button.setAttribute("id","up_button");
        fifth_button.setAttribute("class",i.toString());
        fifth_image = document.createElement("img");
        fifth_image.setAttribute("id","up");
        fifth_image.setAttribute("class",i.toString());
        fifth_image.setAttribute("src","../static/up_arrow.svg");
        fifth_button.appendChild(fifth_image);
        third_button.appendChild(third_image);
        checkbox = document.createElement("button");
        checkbox.setAttribute("id","checkbox_button");
        checkbox_image = document.createElement("img");
        checkbox_image.setAttribute("id","checkbox");
        checkbox_image.setAttribute("class",i.toString());
        checkbox.appendChild(checkbox_image);
        second_div.appendChild(second_input);
        third_div.appendChild(third_button);
        fourth_div.appendChild(fourth_input);
        fifth_div.appendChild(fifth_button);
        sixth_div.appendChild(checkbox);
        parent = document.getElementsByClassName("col-lg-11")[0];
        main_div.appendChild(second_div);
        main_div.appendChild(third_div);
        main_div.appendChild(fourth_div);
        main_div.appendChild(fifth_div);
        main_div.appendChild(sixth_div);
        //subtracting 2 from the length was trial and error
        parent.insertBefore(main_div,parent.childNodes[parent.childNodes.length-2]);
    }
}
/*
sample of what it creates in html
                <div class="d-flex justify-content-center">
                    <div class="p-2">
                        <input type="text" class="form-control" id="usr" readonly>
                    </div>
                    <div class="p-2">
                        <button id="down_button"><img id="down" src="../static/down_arrow.svg"></button>
                    </div>
                    <div class="p-2">
                        <input type="text" class="form-control" id="usr" readonly>
                    </div>
                    <div class="p-2">
                        <button id="down_button"><img id="up" src="../static/up_arrow.svg"></button>
                    </div>
                    <div class="p-2">
                        <button id="down_button"><img id="checkbox" src=""></button>
                    </div>                    
                </div>
*/

//synonymous to window.onload
socket.on('connect',function() {
    socket.emit('message',username);
});

//after connect function, python will send a message which is analyzed by this function
socket.on('groceries', function(msg) {
    create(msg);
});

//clicking on the up and down buttons will add or subtract 1 from quantity
$(document).on('click', '#down_button', function() {
    id = this.getAttribute("class");
    console.log(id)
    document.getElementById(id).value = parseInt(document.getElementById(id).value)-1;
});

$(document).on('click', '#up_button', function() {
    id = this.getAttribute("class");
    document.getElementById(id).value = parseInt(document.getElementById(id).value)+1; 
});

//submitting final grocery list back to python
$(document).on('click', '#submit_button', function() {
    parent = document.getElementsByClassName("col-lg-11")[0];
    data = {}
    for (var t=5;t < parent.childNodes.length-2;t++){
        data[parent.childNodes[t].childNodes[0].childNodes[0].value] = parent.childNodes[t].childNodes[2].childNodes[0].value;
    }
    data["username"] = localStorage.getItem("username");
    console.log(data);
    socket.emit('json', data);
});

//to add new item to grocery list
$(document).on('click', '#go', function() {
    item = document.getElementById("add_item").value;
    list = [[item,1]];
    create(list);
}); 

//show that server has successfully saved the new grocery list
socket.on('notification',function(){
    alert = document.getElementsByClassName("alert alert-success")[0];
    alert.setAttribute("style","display:block");
});
