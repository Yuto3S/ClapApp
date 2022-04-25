import { capFirst, encode, generateRandomId, getRandomInt, generateName } from "./js/utils.js";
import { getWebSocketServer, joinRoom, waitHandleUserActions } from "./js/websocket.js"

window.addEventListener("DOMContentLoaded", () => {
    const websocket = new WebSocket(getWebSocketServer());
    generateDefaultUserParameters();

    joinRoom(websocket);

    playClappInit(websocket);
    updateNameInit(websocket)
    updatePictureInit(websocket);

    waitHandleUserActions(websocket);

    websocket.onclose = function(event) {
        document.getElementById("disconnected").classList.remove("hidden");
        document.getElementById("invitationArea").classList.add("hidden");
    };

    document.getElementById("receiver").addEventListener("click", ({target}) => {
        const button = target;
        const buttonComponent = document.getElementById(button.id);
        const link = document.getElementById(button.id + "_link").href;
        navigator.clipboard.writeText(link);
        buttonComponent.innerHTML = "Copied invitation!";

        const animation = "animate-bounce";
        buttonComponent.classList.add(animation);

        setTimeout(() => {
            buttonComponent.innerHTML = "Copy invitation link";
            buttonComponent.classList.remove(animation);
        }, 1500);
    });

    document.getElementById("emitter").addEventListener("click", ({target}) => {
        const button = target;
        const buttonComponent = document.getElementById(button.id);
        const link = document.getElementById(button.id + "_link").href;
        navigator.clipboard.writeText(link);
        buttonComponent.innerHTML = "Copied invitation!";

        const animation = "animate-bounce";
        buttonComponent.classList.add(animation);

        setTimeout(() => {
            buttonComponent.innerHTML = "Copy invitation link";
            buttonComponent.classList.remove(animation);
        }, 1500);
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


function playClappInit(websocket){
    const sounds = document.getElementById('sounds').children;
    for (let sound of sounds) {
        sound.addEventListener("click", ({ target }) => {
            const event = {
                action: "clap",
                sound: target.id,
            }
            websocket.send(JSON.stringify(event));
        });
    }
}

function updateNameInit(websocket){
    var event = {
        action: "update",
        update: "username",
        username: null,
        user_id: encode(document.getElementById("user_id").value),
    };

    document.getElementById('username').addEventListener("change", ({ target }) => {
        event.username = document.getElementById('username').value;
        localStorage.setItem("username", event.username);
        websocket.send(JSON.stringify(event));
    })
}

function updatePictureInit(websocket){
    const profilePicture = document.getElementById("profile_picture");
    const user_id = document.getElementById("user_id").value;
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
                const event = {
                    action: "update",
                    update: "picture",
                    picture: reader.result,
                    user_id: encode(user_id),
                }
                websocket.send(JSON.stringify(event));
            };
        }
    })
}
