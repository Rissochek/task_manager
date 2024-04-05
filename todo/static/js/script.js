var modal = document.getElementById("description");
var closeBtn = document.getElementsByClassName("close")[0];
var openButtons = document.getElementsByClassName("open-modal");

closeBtn.onclick = function () {
    modal.style.display = "none";
}

for (var i = 0; i < openButtons.length; i++) {
    openButtons[i].onclick = function () {
        modal.style.display = "block";
    }
}

window.onclick = function (event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}