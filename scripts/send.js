const btn = document.getElementById("send")
const infoField = document.getElementById("InfoText")

const time = document.getElementById("time")
const date = document.getElementById("date")
const tel = document.getElementById("tel")
function printInfo(e){
    if (time.value && date.value && tel.value){
    infoField.innerText = "Данные были отправлены, в ближайшее время врач свяжется с вами!"
    
    }
    else {console.log("worng")}
}


btn.addEventListener("click", printInfo)