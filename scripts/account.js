import exampleJsonFile from '../db/users.json' assert { type: "json" };
const name = document.getElementById('name')
const sec = document.getElementById('sec')
const tri = document.getElementById('tri')
const age = document.getElementById('age')
const tel = document.getElementById('tel')
const snils = document.getElementById('snils')
const passport1 = document.getElementById('passport1')
const addr = document.getElementById('addr')
const med = document.getElementById('med')
const passport2 = document.getElementById('passport2')
const full_name = document.getElementById('full_name')
const born = document.getElementById('born')
try {
    full_name.innerText += exampleJsonFile["users"][0]["full_name"]
    born.innerText += exampleJsonFile["users"][0]["born"]
    console.log("OK => Not full Account")
}
catch {
    name.innerText += exampleJsonFile["users"][0]["full_name"].split(' ')[0]
    sec.innerText += exampleJsonFile["users"][0]["full_name"].split(' ')[1]
    tri.innerText += exampleJsonFile["users"][0]["full_name"].split(' ')[2]
    age.innerText += exampleJsonFile["users"][0]["age"]
    tel.innerText += exampleJsonFile["users"][0]["tel"]
    snils.innerText += exampleJsonFile["users"][0]["snils"]
    passport1.innerText += exampleJsonFile["users"][0]["passport"].split(' ')[0]
    passport2.innerText += exampleJsonFile["users"][0]["passport"].split(' ')[1]
    med.innerText += exampleJsonFile["users"][0]["med"]
    addr.innerText += exampleJsonFile["users"][0]["addr"]
    console.log("OK => Full Account")
}