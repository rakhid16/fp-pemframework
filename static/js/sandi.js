function Lihat_Sandi() {
  var x = document.getElementById("Sandi_Admin");
  if (x.type === "password") {
    x.type = "text";
  } else {
    x.type = "password";
  }
}

// Buat admin
var password = document.getElementById("sandi_baru")
, confirm_password = document.getElementById("sandi_baru_2");

function Cek_Sandi(){
  if(password.value != confirm_password.value) {
    confirm_password.setCustomValidity("Sandi tidak cocok");
  } else {
    confirm_password.setCustomValidity('');
  }
}

password.onchange = Cek_Sandi;
confirm_password.onkeyup = Cek_Sandi;