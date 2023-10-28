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
    document.querySelector("#account--signup").value = "";
    document.querySelector("#email--signup").value = "";
    document.querySelector("#password--signup").value = "";
    signinFile.setAttribute('style',"display:none;");
    document.querySelector("#email--signin").value = "";
    document.querySelector("#password--signin").value = "";
}
