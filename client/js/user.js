function addNewUser(user) {
    const picture = user.picture != undefined ? user.picture : "./client/assets/clap.png";
    var userElement = document.getElementById(user.id);
    var online_user_list2 = document.getElementById("online_users_2");
    console.log("online_user_list2");
    console.log(online_user_list2);

    const node = document.createElement("div");
    online_user_list2.appendChild(node);
    node.outerHTML = `
        <div id="${user.id}" class="bg-sky-800 p-2 max-w-sm rounded-xl mx-auto shadow-lg grid-item flex items-center">
            <img class="h-16 w-16 object-cover rounded-full" src="${picture}" alt="Current profile photo" />
            <h3 class="m-2 text-white text-base font-medium tracking-tight">${user.name}</h3>
        </div>`;
}

/// TODO: refactor both updateSingleUser & updateOnlineUsers into one
function updateSingleUser(user) {
    const picture = user.picture != undefined ? user.picture : "./client/assets/clap.png";
    var userElement = document.getElementById(user.id);
    console.log("userElement");
    console.log(userElement);
//    debugger;
    if(userElement == null){
        var online_user_list2 = document.getElementById("online_users_2");
        console.log("online_user_list2");
        console.log(online_user_list2);

        const node = document.createElement("div");
        online_user_list2.appendChild(node);
        node.outerHTML = `
            <div id="${user.id}" class="bg-sky-800 p-2 max-w-sm rounded-xl mx-auto shadow-lg grid-item flex items-center">
                <img class="h-16 w-16 object-cover rounded-full" src="${picture}" alt="Current profile photo" />
                <h3 class="m-2 text-white text-base font-medium tracking-tight">${user.name}</h3>
            </div>`;
    }
    else {
        userElement.innerHTML = `
            <img class="h-16 w-16 object-cover rounded-full" src="${picture}" alt="Current profile photo" />
            <h3 class="m-2 text-white text-base font-medium tracking-tight">${user.name}</h3>
        `;
    }
}

function updateOnlineUsers(onlineUsers) {
    var result = "";
    console.log("update all users");
    console.log(onlineUsers);
    onlineUsers.forEach(function(user){
        var picture = user.picture != undefined ? user.picture : "./client/assets/clap.png";
        result += `
            <div id="${user.id}" class="bg-sky-800 p-2 max-w-sm rounded-xl mx-auto shadow-lg grid-item flex items-center">
                <img class="h-16 w-16 object-cover rounded-full" src="${picture}" alt="Current profile photo" />
                <h3 class="m-2 text-white text-base font-medium tracking-tight">${user.name}</h3>
            </div>`;
    })
    var online_user_list2 = document.getElementById("online_users_2");
    online_user_list2.innerHTML = result;
}

function deleteUser(user) {
    const toDelete = document.getElementById(user.id);
    toDelete.parentNode.removeChild(toDelete);
}

function clap(sound){
    console.log(sound);
    const promise = document.getElementById(sound+"_audio").play();
    if (promise !== undefined) {
        promise.then(_ => {
            document.getElementById("error_sound").classList.add("hidden");
        }).catch(error => {
            document.getElementById("error_sound").classList.remove("hidden");
        });
    }
}

export { clap, deleteUser, updateSingleUser, addNewUser, updateOnlineUsers };
