let userName = document.getElementById("userName")
let userspan = document.querySelector("#userSpan")
let pass = document.getElementById("password")
let passSpan = document.querySelector("#passSpan")
function users() {
    if (userName.value.length < 12) {
        userspan.innerHTML = "نام کاربری باید دوازده کارکتر باشد"
        userspan.style.color = "red"
    } else {
        userspan.innerHTML = "درست است"
        userspan.style.color = "green"
    }
    userspan.style.display = "block"
}
function passwor() {
    if (pass.value.length < 8) {
        passSpan.innerHTML = "رمز عبور باید هشت کارکتر باشد"
        passSpan.style.color = "red"
    } else {
        passSpan.innerHTML = "درست است"
        passSpan.style.color = "green"
    }
    passSpan.style.display = "block"
}
pass.addEventListener("blur", function passBlur() {
    passSpan.style.display = "none"
})
userName.addEventListener("blur", function userBlur() {
    userspan.style.display = "none"
})