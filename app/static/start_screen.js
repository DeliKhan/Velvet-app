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
window.onclick = function(event) {
    input = document.getElementById("recipe");
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
