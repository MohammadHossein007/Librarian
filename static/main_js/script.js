let img1 = document.getElementById("img")
let daste=document.getElementById("ganr")
 let flag=false
function image() {
    if (flag) {
        img1.style.transform="rotate(0deg)"
        daste.style.opacity="0%"
        flag = false
        
    } else {
        img1.style.transform="rotate(180deg)"
        daste.style.opacity="100%"
        flag = true
        
    }
} 