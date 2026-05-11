function validateSignup(){

let email =
document.getElementById("email").value;

let password =
document.getElementById("password").value;

let error =
document.getElementById("error");

if(!email.includes("@gmail.com")){

error.innerHTML =
"Enter valid Gmail";

error.style.color = "red";

return false;
}

if(password.length < 8){

error.innerHTML =
"Password must contain minimum 8 characters";

error.style.color = "red";

return false;
}

return true;
}