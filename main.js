const audio = new Audio('clapping.mp3');


window.addEventListener("DOMContentLoaded", () => {
    const websocket = new WebSocket("ws://localhost:8001");
    websocket.addEventListener("message", ({data}) => {
        const event = JSON.parse(data);
        console.log(event);
        console.log("cool");
        if(event.active != undefined) {
            document.querySelector(".active").href = "?active=" + event.active;
        }
    })

    const clapp = document.getElementById('clapp');
    console.log(clapp);
    initClappers(websocket);
    playClappInit(websocket, clapp);
    playClappPassive(websocket);
});

function initClappers(websocket) {
    websocket.addEventListener("open", () => {
        const event = {
            type: "init",
        }

        const params = new URLSearchParams(window.location.search);
        if (params.has("active")) {
            event.active = params.get("active")
        }
        console.log(event);
        websocket.send(JSON.stringify(event));
    });
}

function playClappPassive(websocket){
    websocket.addEventListener("message", ({ data }) => {
        const event = JSON.parse(data);
        if (event.action == "clap") {
            document.getElementById("clapping1").play();
        }
    })
}

function playClappInit(websocket, clapp){
    clapp.addEventListener("click", ({ target }) => {
        console.log("click");
        const event = {
            type: "clap",
        }
        websocket.send(JSON.stringify(event));
    });

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
}
