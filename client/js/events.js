import { getUserId } from "./user.js"

function getInitRoomEvent(){
    return {
        type: "init",
        username: localStorage.getItem("username"),
        user_id: getUserId(),
        picture: localStorage.getItem("picture") ? localStorage.getItem("picture") : null,
    };
}

function getUpdateNameEvent(newName){
    return {
        action: "update",
        update: "username",
        username: newName,
        user_id: getUserId(),
    };
}

function getPlaySoundEvent(soundId){
    return {
        action: "clap",
        sound: soundId,
    };
}

function getUpdatePictureEvent(newPicture){
    return {
        action: "update",
        update: "picture",
        picture: newPicture,
        user_id: getUserId(),
    };
}

export { getInitRoomEvent, getUpdatePictureEvent, getUpdateNameEvent, getPlaySoundEvent }
