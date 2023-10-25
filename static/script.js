//產生遮幕
function createShield(){
    const shield= document.createElement('div');
    const setShieldStyle = "position:fixed;top:0px;width:100%;height:100%;z-index:2;background-color:rgba(0,0,0,0.5)";
    shield.setAttribute('style',`${setShieldStyle}`);
    shield.setAttribute('id',"shield");
    body.appendChild(shield);
    shield.addEventListener('click',removeFile)
}
//使遮幕及表單消失
function removeFile(){
    const shield = document.querySelector("#shield");
    body.removeChild(shield);
    newMessageFile.setAttribute('style',"display:none;");
    fakeInput.setAttribute('style',"display:flex;");
    preview.setAttribute('style',"display:none;");
    signupFile.setAttribute('style',"display:none;");
    accountSignup = "";
    emailSignup = "";
    passwordSignup = "";
    signinFile.setAttribute('style',"display:none;");
    emailSignin = "";
    passwordSignin = "";
}

//建立留言監聽事件
newMessage.addEventListener('click',()=>{
    const setFileStyle = "display:flex;"
    newMessageFile.setAttribute('style',`${setFileStyle}`);
    const messageInput = document.querySelector('#fileInput');
    messageInput.setAttribute('placeholder',"請幫這張照片做一些說明");
    messageInput.addEventListener('click',()=>{
        messageInput.setAttribute('placeholder',"");
    })
    createShield();
})
//獲取新留言放入的相片資訊
const addImg = document.querySelector("#fileImg");
addImg.addEventListener('change', function() {
    const file = this.files[0];
    const reader = new FileReader();

    reader.onload = function() {
        fakeInput.setAttribute('style',"display:none;")
        preview.src = reader.result;
        preview.style= "display:block;width:400px;height:300px;object-fit:cover";
    }
    if (file) {
        reader.readAsDataURL(file);
    }
});
//監聽分享按鈕點擊事件
share.addEventListener('click',()=>{
    console.log(preview.src);
    const addText = document.querySelector("#fileInput");
    console.log(addText.value);
    const shield = document.querySelector('#shield');
    body.removeChild(shield);
    newMessageFile.setAttribute('style',`display:none`);
    messageRecord("zhou",preview.src,addText.value);
})

signup.addEventListener('click',()=>{
    signupFile.setAttribute('style',`display:flex`);
    createShield();
    const memberSignup = document.querySelector("#signup");
    memberSignup.addEventListener('click',()=>{
        const alert = document.querySelector("#signupAlert");
        if(!accountSignup||!emailSignup||!passwordSignup){
            alert.textContent = "請確認資料都有完整填寫";
            alert.setAttribute('style',"color:red;")
        }else{
            let count = 0;
            for(let w=0;w<email.length;w++){
                if(email[w]==="@"){count++;}
            }
            if(count !== 1){
                alert.textContent = "email格式不正確";
                alert.setAttribute('style',"color:red;")
            }else{
                fetch("/api/user",{
                    method:"POST",
                    body:JSON.stringify({
                                    "account":accountSignup,
                                    "email":emailSignup,
                                    "password":passwordSignup
                                }),
                                headers:{
                                    "Content-Type":"application/json"
                                }
                }).then(response=>response.json()
                ).then(result=>{
                    if(result.error){
                        alert.textContent = `${result.message}`;
                        alert.setAttribute('style',"color:red;");
                    }else{
                        alert.textContent = `${result.data}`;
                        alert.setAttribute('style',"color:green;");
                        setTimeout(removeFile,1000)
                    }
                })
            }
        }
    })
})

signin.addEventListener('click',()=>{
    signinFile.setAttribute('style',`display:flex`);
    createShield();
    const memberSignin = document.querySelector("#signin");
    memberSignin.addEventListener('click',()=>{
        const alert = document.querySelector("#signinAlert");
        if(!emailSignin||!passwordSignin){
            alert.textContent = "請確認資料都有完整填寫";
            alert.setAttribute('style',"color:red;")
        }else{
            fetch('/api/user/auth',{
                method:"PUT",
                body:JSON.stringify({
                    "email":emailSignin,
                    "password":passwordSignin
                }),
                headers:{
                    "Content-Type":"application/json"
                }
            }).then(response=>response.json())
            .then(result=>{
                if(result.error){
                    alert.textContent = `${result.message}`;
                    alert.setAttribute('style',"color:red;");
                }else{
                    let token = data.token;
                    localStorage.setItem('token', token);
                    alert.textContent = "登入成功";
                    alert.setAttribute('style',"color:green;");
                    setTimeout(removeFile,1000);
                    
                }
            })
        }
    })
})
