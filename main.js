function copyRoomLinkToClipboard(button) {
    var clapper_key = document.getElementById(button.id + "_link");
    navigator.clipboard.writeText(clapper_key.href);
    var tooltip = document.getElementById(button.id + "Tooltip");
    tooltip.innerHTML = "Copied room invitation: " + clapper_key.href;
    tooltip.classList.add("show_tool_tip");
    console.log(clapper_key.href);
}

function hideTooltip(button) {
    var tooltip = document.getElementById(button.id + "Tooltip");
    tooltip.classList.remove("show_tool_tip");
}

function getWebSocketServer(){
    console.log(window.location.host)
    if (window.location.host === "yuto3s.github.io") {
        return "wss://yuto3s-clapapp.herokuapp.com";
    } else if (window.location.host === "localhost:8000") {
        return "ws://localhost:8001";
    } else {
        throw new Error(`Unsupported host: ${window.location.host}`);
    }
}

window.addEventListener("DOMContentLoaded", () => {
    const websocket = new WebSocket("wss://yuto3s-clapapp.herokuapp.com");

    initWebSocket(websocket);
    initWebSocketMessageListeners(websocket);
    playClappInit(websocket);
});

function initWebSocketMessageListeners(websocket) {
    websocket.addEventListener("message", ({ data }) => {
        const event = JSON.parse(data);
        if (event.action == "clap") {
            clap();
        }

        /** Logic used on the first user initiating a new room **/
        if (event.emitter != undefined) {
            document.querySelector(".emitter").href = "?emitter=" + event.emitter + "&receiver=" + event.receiver;
            document.querySelector(".receiver").href = "?receiver=" + event.receiver;
        }
    })
}


function initWebSocket(websocket) {
    websocket.addEventListener("open", () => {
        const event = {
            type: "init",
        }

        /** Logic used whenever a user joins a room from a specific URL **/
        const params = new URLSearchParams(window.location.search);
        console.log(params.values());
        if (params.has("emitter")) {
            event.emitter = params.get("emitter");
            event.receiver = params.get("receiver");
            document.querySelector(".emitter").href = "?emitter=" + event.emitter + "&receiver=" + event.receiver;
            document.querySelector(".receiver").href = "?receiver=" + event.receiver;
        } else if (params.has("receiver")) {
            event.receiver = params.get("receiver");
            document.querySelector(".receiver").href = "?receiver=" + event.receiver;

            /** A receiver can't play sound or invite emitters, so we hide those buttons **/
            var soundButton = document.getElementById("clapp");
            var emitterButton = document.getElementById("emitter");
            soundButton.style.display = "none";
            emitterButton.style.display = "none";
        }
        console.log(event);
        websocket.send(JSON.stringify(event));
    });
}

function playClappInit(websocket){
    const clapp = document.getElementById('clapp');
    clapp.addEventListener("click", ({ target }) => {
        console.log("click");
        const event = {
            action: "clap",
        }
        websocket.send(JSON.stringify(event));
    });
}

function clap(){
    console.log("clap");
    const promise = document.getElementById("clapping1").play();
    if (promise !== undefined) {
        promise.then(_ => {
            console.log("autoplay");
        }).catch(error => {
            console.log(error);
        });
    }
}
