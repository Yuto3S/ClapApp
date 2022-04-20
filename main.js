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

window.addEventListener("DOMContentLoaded", () => {
    console.log("ok");
    const websocket = new WebSocket("ws://localhost:8001");

    initWebSocket(websocket);
    initWebSocketMessageListeners(websocket);
    playClappInit(websocket);
});

function initWebSocketMessageListeners(websocket) {
    websocket.addEventListener("message", ({ data }) => {
        const event = JSON.parse(data);
        console.log(event);
        if (event.action == "clap") {
            console.log("clap");
            document.getElementById("clapping1").play();
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

//        const promise = clapp.play();
//        if (promise !== undefined) {
//            promise.then(_ => {
//                console.log("autoplay");
//            }).catch(error => {
//                console.log(error);
//                var isOpera = (!!window.opr && !!opr.addons) || !!window.opera || navigator.userAgent.indexOf(' OPR/') >= 0;
//                // Firefox 1.0+
//                var isFirefox = typeof InstallTrigger !== 'undefined';
//                // Safari 3.0+ "[object HTMLElementConstructor]"
//                var isSafari = /constructor/i.test(window.HTMLElement) || (function (p) { return p.toString() === "[object SafariRemoteNotification]"; })(!window['safari'] || (typeof safari !== 'undefined' && window['safari'].pushNotification));
//                // Internet Explorer 6-11
//                var isIE = /*@cc_on!@*/false || !!document.documentMode;
//                // Edge 20+
//                var isEdge = !isIE && !!window.StyleMedia;
//                // Chrome 1 - 79
//                var isChrome = !!window.chrome && (!!window.chrome.webstore || !!window.chrome.runtime);
//                // Edge (based on chromium) detection
//                var isEdgeChromium = isChrome && (navigator.userAgent.indexOf("Edg") != -1);
//                // Blink engine detection
//                var isBlink = (isChrome || isOpera) && !!window.CSS;
//
//                var output = 'Detecting browsers by ducktyping:<hr>';
//                output += 'isFirefox: ' + isFirefox + '<br>';
//                output += 'isChrome: ' + isChrome + '<br>';
//                output += 'isSafari: ' + isSafari + '<br>';
//                output += 'isOpera: ' + isOpera + '<br>';
//                output += 'isIE: ' + isIE + '<br>';
//                output += 'isEdge: ' + isEdge + '<br>';
//                output += 'isEdgeChromium: ' + isEdgeChromium + '<br>';
//                output += 'isBlink: ' + isBlink + '<br>';
//                console.log(output);
//                console.log("Please enable autoplay of sounds")
//            });
//        }
//}
