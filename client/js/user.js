import { encode } from "./utils.js"

function getUserId() {
    return encode(document.getElementById("user_id").value);
}

function getUserOuterHtml(user, picture){
    return `
        <div id="${user.id}" class="bg-sky-800 p-2 max-w-sm rounded-xl mx-auto shadow-lg grid-item flex items-center">
            ${getUserInnerHtml(user)}
        </div>`
}

function getUserInnerHtml(user){
    const picture = user.picture != undefined ? user.picture : "./client/assets/clap.png";

    return `
        <img class="h-16 w-16 object-cover rounded-full" src="${picture}" alt="Current profile photo" />
        <h3 class="m-2 text-white text-base font-medium tracking-tight">${user.name}</h3>
    `
}

function addNewUser(user) {
    const node = document.createElement("div");
    document.getElementById("online_users_2").appendChild(node);

    node.outerHTML = getUserOuterHtml(user);
}

function updateSingleUser(user) {
    document.getElementById(user.id).innerHTML = getUserInnerHtml(user);
}

function updateOnlineUsers(onlineUsers) {
    onlineUsers.forEach(function(user){
        addNewUser(user);
    })
}

function deleteUser(user) {
    const userToDelete = document.getElementById(user.id);
    userToDelete.parentNode.removeChild(userToDelete);
}

function clap(sound){
    const promise = document.getElementById(`${sound}_audio`).play();
    if (promise !== undefined) {
        promise.then(_ => {
            document.getElementById("error_sound").classList.add("hidden");
        }).catch(error => {
            document.getElementById("error_sound").classList.remove("hidden");
        });
    }
}

export { clap, deleteUser, updateSingleUser, addNewUser, updateOnlineUsers, getUserId };
