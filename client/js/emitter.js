import { updateReceiverLink } from "./receiver.js"

function joinEmitterExistingRoom(params, event) {
    event.emitter = params.get("emitter");
    event.receiver = params.get("receiver");
    updateEmitterLink(event);
    updateReceiverLink(event);
};

function updateEmitterLink(event) {
    document.getElementById("emitter_link").href = "?emitter=" + event.emitter + "&receiver=" + event.receiver;
}

export { joinEmitterExistingRoom, updateEmitterLink };
