const newMessage = document.querySelector("#add");
const newMessageFile = document.querySelector(".file");
const fakeInput = document.querySelector(".fileUpload")
const preview = document.getElementById('previewImg');
const body = document.querySelector("body");
const container = document.querySelector(".container");
const signup = document.querySelector("#signupBTN");
const signupFile = document.querySelector(".signupfile");
const signin = document.querySelector("#signinBTN");
const signinFile = document.querySelector(".signinfile");
const signout = document.querySelector("#signoutBTN");

//建立頁面動態留言
function messageRecord(account,img_src,messageText){
    const userphoto = document.createElement('img');
    userphoto.setAttribute('class',"userphoto");
    userphoto.setAttribute('src',"../static/image/user.png");
    const username = document.createElement('span');
    username.setAttribute('class',"username bold");
    username.textContent = account;
    const usernav = document.createElement('div');
    usernav.setAttribute('class',"usernav");
    usernav.appendChild(userphoto);
    usernav.appendChild(username);

    const usercontain = document.createElement('div');
    usercontain.setAttribute('class',"usercontain");
    const messageImg = document.createElement('img');
    messageImg.setAttribute('class',"messageImg");
    messageImg.setAttribute('src',img_src)
    const message = document.createElement('div');
    message.setAttribute('class',"message");
    const text = document.createElement('span');
    text.setAttribute('class',"text");
    text.textContent = messageText;
    const usernameClone = username.cloneNode(true);
    message.appendChild(usernameClone);
    message.appendChild(text);
    usercontain.appendChild(messageImg);
    usercontain.appendChild(message);

    const messageRecord = document.createElement('div');
    messageRecord.setAttribute('class',"messageRecord");
    messageRecord.appendChild(usernav);
    messageRecord.appendChild(usercontain);

    container.appendChild(messageRecord);
}
messageRecord("zhou","../static/image/testPhoto.jpg","悠閒午後 輕鬆隨手畫");
messageRecord("zhou","../static/image/testPhoto_2.jpg","你的幸運貓貓來了!!!");

async function init(){
    let records = await fetch("/api/record",
        {method: "GET",headers: {"Content-Type": "application/json"}}
    )
    let recordJSON = await records.json();
    for(let record in recordJSON){
        messageRecord("zhou",recordJSON[record]['picture'],recordJSON[record]['text'])
    }
}
init();
