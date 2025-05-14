let state = {};

function add_new_line(number_of_letters) {
    if (document.getElementById("new_row")){
        remove_new_line()
    }
    const column = document.getElementById("lettercolumncontainer");
    const new_row = document.createElement("div");
    column.appendChild(new_row);
    new_row.setAttribute("id", "new_row");

    for (i in [...Array(number_of_letters)]) {
        const new_letter = document.createElement("div");
        new_letter.setAttribute("class", "letterbox");
        new_row.appendChild(new_letter);
    }
    
}

function remove_new_line() {
    const column = document.getElementById("lettercolumncontainer");
    const new_row = document.getElementById("new_row");
    if (new_row != null) {
        column.removeChild(new_row);
    }
}

function reset_interface() {
    const element = document.getElementById("lettercolumncontainer");
    while (element.firstChild) {
        element.removeChild(element.firstChild);
      }

    add_new_line();
}

function update_interface(new_state) {
    remove_new_line();
    for (const key in new_state) {
        if (state[key] || key[0] == "_") {
            continue;
        }
        var new_row = document.createElement("div");
        const id = "id" + new_state._hash.toString();
        new_row.setAttribute("id", id);
        new_row.setAttribute("class", "letterrowcontainer");
        document.getElementById("lettercolumncontainer").appendChild(new_row);
        for (const i in [...Array(new_state._answer_length).keys()]) {
            let new_letter;
            if (new_state[key][i] == "True") {
                new_letter = document.createElement("div");
                new_letter.setAttribute("class", "letterbox correct");
                new_letter.innerHTML = key[i];
            } else if (new_state[key][i] == "Partial") {
                new_letter = document.createElement("div");
                new_letter.setAttribute("class", "letterbox partcorrect");
                new_letter.innerHTML = key[i];
            } else {
                new_letter = document.createElement("div");
                new_letter.setAttribute("class", "letterbox incorrect");
                new_letter.innerHTML = key[i];
            }
            document.getElementById(id).appendChild(new_letter);
        }
    }
    add_new_line(new_state._answer_length);
}

async function update_game_state() {
    const response = fetch("./game/")
        .then(response => response.json())
        .then(data => {
            const new_state = data;
            if (!state || (new_state._game_id != state._game_id)) {
                state = new_state;
                reset_interface();
                add_new_line(new_state._answer_length);
            } else if (new_state._hash != state._hash) {
                for (const key in new_state) {
                    console.log(`${key} : ${new_state[key]}`);
                }
                document.getElementById("something").innerText = JSON.stringify(new_state);
                update_interface(new_state);
                state = new_state;
            } else if (new_state._running == "false") {
                console.log("Game not running");
            }
        })
    };

setInterval(() => update_game_state(), 2000);