var xmlhttp = new XMLHttpRequest();
var url = "core.php";

xmlhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
        getDbData(this.responseText);
    }
}
xmlhttp.open("GET", url, true);
xmlhttp.send();


function getDbData(response) {
    console.log(response);
}

document.getElementById('posts').appendChild(div);
