function joinReceiverExistingRoom(params, event) {
    event.receiver = params.get("receiver");
    updateReceiverLink(event);

    updateSoundAreaText();
    hideEmitterArea();
    disableSoundButtons();
};

function updateSoundAreaText() {
    const soundClickTextAreaEmitter = document.getElementById("emitter_sound_text");
    soundClickTextAreaEmitter.classList.add("hidden");

    const soundClickTextAreaListener = document.getElementById("listener_sound_text");
    soundClickTextAreaListener.classList.remove("hidden");
}

function hideEmitterArea() {
    const emitterArea = document.getElementById("emitterArea");
    emitterArea.classList.add("hidden");
    const invitationArea = document.getElementById("invitationArea");
    invitationArea.classList.remove("columns-2")
}

function disableSoundButtons(){
    const sounds = document.getElementById('sounds').children;

    for (const sound of sounds) {
        sound.classList.remove("hover:bg-sky-700");
        sound.classList.add("cursor-not-allowed");
    }
}

function updateReceiverLink(event) {
    document.getElementById("receiver_link").href = "?receiver=" + event.receiver;
}

export { joinReceiverExistingRoom, updateReceiverLink };
