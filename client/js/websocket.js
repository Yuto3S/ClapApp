import { joinEmitterExistingRoom, updateEmitterLink } from "./emitter.js"
import { joinReceiverExistingRoom, updateReceiverLink } from "./receiver.js"
import { encode } from "./utils.js"
import { clap, deleteUser, updateSingleUser, addNewUser, updateOnlineUsers } from "./user.js";

function getWebSocketServer(){
    if (window.location.host === "yuto3s.github.io") {
        return "wss://yuto3s-clapapp.herokuapp.com";
    } else if (window.location.host === "localhost:8000") {
        return "ws://localhost:8001";
    } else {
        throw new Error(`Unsupported host: ${window.location.host}`);
    }
}

function joinRoom(websocket) {
    websocket.onopen = function() {
        const event = {
            type: "init",
            username: localStorage.getItem("username"),
            user_id: encode(document.getElementById("user_id").value),
            picture: localStorage.getItem("picture") ? localStorage.getItem("picture") : null,
        }

        const params = new URLSearchParams(window.location.search);
        if (params.has("emitter")) {
            joinEmitterExistingRoom(params, event);
        } else if (params.has("receiver")) {
            joinReceiverExistingRoom(params, event);
        }
        websocket.send(JSON.stringify(event));
    };
}

function waitHandleUserActions(websocket) {
    websocket.onmessage = function(data) {
        const event = JSON.parse(data.data);
        if (event.action == "init") {
            updateReceiverLink(event);
            updateEmitterLink(event);
        } else if (event.action == "clap") {
            clap(event.sound);
        } else if (event.action == "delete") {
            deleteUser(event.user);
        } else if (event.action == "add") {
            addNewUser(event.user);
        } else if (event.action == "update") {
            if (event.update == "all_users"){
                updateOnlineUsers(event.users);
            } else if (event.update == "single_user") {
                updateSingleUser(event.user);
            }
        }
    };
}

export { getWebSocketServer, joinRoom, waitHandleUserActions };
