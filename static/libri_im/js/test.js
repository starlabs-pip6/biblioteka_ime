const password = document.getElementById("password");
const togglePassword = document.getElementById("toggle-password");

togglePassword.addEventListener("click", toggleClicked);

function toggleClicked() {  
    if (this.checked) {
      password.type = "text";
    } else {
      password.type = "password";
    }
  }
  password.classList.toggle('visible'); 