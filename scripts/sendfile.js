const btn = document.getElementById("send")
const infoField = document.getElementById("InfoText")

const file = document.getElementById("file")
const text = document.getElementById("text")
function printInfo(e){
    if (file.value && text.value){
    infoField.innerText = "Данные были отправлены, в ближайшее время врач свяжется с вами!"
    
    }
    else {console.log("worng")}
}


btn.addEventListener("click", printInfo)