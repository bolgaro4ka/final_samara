import exampleJsonFile from '../../db/users.json' assert { type: "json" };
const button = document.getElementById("continueSignUp");
const nameField=document.getElementById("name");
const passField = document.getElementById("pass");
const infoField = document.getElementById("info")
var names=[]; var passs=[]
for(let i = 0; exampleJsonFile.users.length > i; i++){
    names.push(exampleJsonFile.users[i].name)
    passs.push(exampleJsonFile.users[i].pass)
}

function no(){
    infoField.innerText = "Неверный пароль или адрес электронной почты"
}



function enter(e){
    console.log(exampleJsonFile.users.length)
    console.log(nameField.value, names.find((i) => i === nameField.value))
    if (names.find((i) => i === nameField.value)){
        if (passs.find((i) => i === passField.value)){
            window.location.href = "../../cabinet.html"
        }
        else{no()}
    }
    else {no()}
}



button.addEventListener("click", enter)
