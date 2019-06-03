// Get the modal
var modal = document.getElementById('id01');

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

$(document).on('click', '#submit', function() {
    var username = document.getElementById('uname').value;
    localStorage.setItem("username", username);
});

$(document).on('click', '#submit_button', function() {
    var search = document.getElementById("recipe").value;
    location.href = ("/search?name=" + search);
});    
