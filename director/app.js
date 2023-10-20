function request(data, callback) {
    let xhr = new XMLHttpRequest();
    xhr.open("POST", window.location.href, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            let response = xhr.responseText;
            callback(JSON.parse(response));
        }
    };
    xhr.send(JSON.stringify(data));
}

function process_board(){
    let dom = document.getElementById('process-board');
    request({command:'process-board'},function (response) {
        if(response.code !== 0){
            alert(response.message);
            return;
        }

        let data = response.data;
        let html = '';
        for (const d in data){
            let panel = `<div class="box"><div class="process"><span class="letters">{message}</span><i class="{type}"></i></div></div>`;
            html += panel.replace("{message}", d + ' --- ' + data[d])
        }
        dom.innerHTML = html;
    });
}

document.addEventListener("DOMContentLoaded", function() {
    process_board();
});
setInterval(()=>{
    process_board();
},30000);