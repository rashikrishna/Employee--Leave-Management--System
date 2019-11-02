

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

function passwordcheck(){
  var x = document.getElementById("v_password");
  if(x.type === "password"){
    x.type = "name";
  }
  else{
    x.type = "password";
  }
}
