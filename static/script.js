document.addEventListener("DOMContentLoaded", function(){

})

function approve(){
  var xhttp = new XMLHttpRequest;
xhttp.onreadystatechange = function() {
  if (this.readyState == 4 && this.status == 200) {
      document.getElementById("confirmation").innerHTML = "One Request Approved !!";
    }
};
xhttp.open("GET","/admin");
xhttp.send();
}


function verify(){
  var xhttp = new XMLHttpRequest;
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        document.querySelector("alert").innerHTML = "Successfully Verified";
      }
  }
  var data = new FormData();
  data.append('flag',1);
  xhttp.open("POST","/verify");
  xhttp.send(data);
}
