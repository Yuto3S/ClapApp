import { capFirst, generateRandomId, getRandomInt, generateName } from "./js/utils.js";
import { getWebSocketServer, joinRoom, handleWebsocketMessageActions } from "./js/websocket.js"
import { getUserId } from "./js/user.js"
import { getInitRoomEvent, getUpdatePictureEvent, getUpdateNameEvent, getPlaySoundEvent } from "./js/events.js"

window.addEventListener("DOMContentLoaded", () => {
    const websocket = new WebSocket(getWebSocketServer());
    generateDefaultUserParameters();

    joinRoom(websocket);
    handleWebsocketMessageActions(websocket);
    handleUserInteractions(websocket)

    websocket.onclose = function(event) {
        document.getElementById("disconnected").classList.remove("hidden");
        document.getElementById("invitationArea").classList.add("hidden");
    };

    document.getElementById("receiver").addEventListener("click", ({target}) => {
        copyRoomLinkToClipboard(target);
    });
    document.getElementById("emitter").addEventListener("click", ({target}) => {
        copyRoomLinkToClipboard(target);
    });
});

function generateDefaultUserParameters() {
    document.getElementById("user_id").value = generateRandomId();

    const defaultPicture = localStorage.getItem("picture") ? localStorage.getItem("picture") : "./client/assets/clap.png";
    document.getElementById("currentpp").src = defaultPicture;

    const userNameInput = document.getElementById('username');
    if (localStorage.getItem("username") == undefined) {
        localStorage.setItem("username", generateName());
    }
    userNameInput.value = localStorage.getItem("username");
}

function handleUserInteractions(websocket) {
    playSoundInitListener(websocket);
    updateNameInitListener(websocket)
    updatePictureInitListener(websocket);
}


function playSoundInitListener(websocket){
    const sounds = document.getElementById('sounds').children;
    for (let sound of sounds) {
        sound.addEventListener("click", ({ target }) => {
            const event = getPlaySoundEvent(target.id);
            websocket.send(JSON.stringify(event));
        });
    }
}

function updateNameInitListener(websocket){
    document.getElementById('username').addEventListener("change", ({ target }) => {
        const event = getUpdateNameEvent(target.value);
        localStorage.setItem("username", target.value);
        websocket.send(JSON.stringify(event));
    })
}

function updatePictureInitListener(websocket){
    document.getElementById('profile_picture').addEventListener("change", ({target}) => {
        const newImage = target.files[0];
        if(newImage.size > 1024 * 1024){
            alert("Image is too big");
        } else {
            var reader = new FileReader();
            reader.readAsDataURL(newImage);
            reader.onload = function () {
                localStorage.setItem("picture", reader.result)
                document.getElementById('currentpp').src = reader.result;
                const event = getUpdatePictureEvent(reader.result)
                websocket.send(JSON.stringify(event));
            };
        }
    })
}

function copyRoomLinkToClipboard(button){
    const buttonComponent = document.getElementById(button.id);
    const link = document.getElementById(`${button.id}_link`).href;
    navigator.clipboard.writeText(link);
    buttonComponent.innerHTML = "Copied invitation!";

    const animation = "animate-bounce";
    buttonComponent.classList.add(animation);

    setTimeout(() => {
        buttonComponent.innerHTML = "Copy invitation link";
        buttonComponent.classList.remove(animation);
    }, 1500);
};
