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
addImg.addEventListener('change', async function() {
    const file = this.files[0];
    let src = await loadFile(file);
    // let img = await loadImage(src); //將src轉為圖片
    // let square = getBase64(img);
    // src = square.src;
    fakeInput.setAttribute('style',"display:none;");
    preview.src = src;
    preview.style= "display:block;width:400px;height:300px;object-fit:cover";
})
function loadFile(file){
    return new Promise((resolve,reject)=>{
        let reader = new FileReader();
        reader.onload = ()=>resolve(reader.result);
        reader.error = reject;
        reader.readAsDataURL(file);
    })
}
function loadImage(src){
    return new Promise((resolve,reject)=>{
        let img = new Image();
        img.onload = ()=>resolve(img);
        img.error = reject;
        img.src = src;
    })
}
function getBase64(img){
    let canvas = document.createElement('canvas');
    let ctx = canvas.getContext('2d');
    let {width, height} = img;
    if(width/height > 4/3){
        let scale = 400/width;
        canvas.width = width * scale;
        canvas.height = height * scale;
    }else{
        let scale = 300/height;
        canvas.width = width * scale;
        canvas.height = height * scale;
    }  
    ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
    return {src:canvas.toDataURL()}
}
//存取新留言
async function storeMessage(formData){
    let store = await fetch("/api/message",
        {method: "POST",
        body: formData,
        }
    )
    let result = await store.json();
    console.log(result);
}

const share = document.querySelector("#share");
share.addEventListener('click',()=>{
    const formData = new FormData();

    let inputFile = addImg.files[0];
    console.log(inputFile)
    const addText = document.querySelector("#fileInput");
    console.log(addText.value);
    formData.append('photo',inputFile);
    formData.append('text',addText.value);

    storeMessage(formData);

    messageRecord("zhen",preview.src,addText.value);
    const shield = document.querySelector('#shield');
    body.removeChild(shield);
    newMessageFile.setAttribute('style',`display:none`);
})