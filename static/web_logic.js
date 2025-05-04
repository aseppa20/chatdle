let state;
async function get_number() {
    const response = fetch("./game/")
        .then(response => response.json())
        .then(data => {
            document.getElementById("something").innerText = JSON.stringify(data);
            //state = data.state_hash;
        })
    };

setInterval(() => get_number(), 2000);