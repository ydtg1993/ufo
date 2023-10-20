function request(data, callback) {
    let xhr = new XMLHttpRequest();
    xhr.open("POST", window.location.href, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.timeout = 60000;
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

        let processes = response.data.process;
        let html = '';
        for (const d in processes){
            let panel = `<div class="box"><div class="process"><span class="letters">{message}</span><i class="{type}"></i></div></div>`;
            panel = panel.replace("{message}", d + ' --- ' + processes[d]['time']);
            let type = 'running';
            if(!processes[d]['live']){
                type = 'stop';
            }
            panel = panel.replace("{type}", d + ' --- ' + type);
            html += panel
        }
        dom.innerHTML = html;
    });
}

let block = {command_stop:false,command_reset_comic:false,command_reset_chapter:false};

function buttonEvent(name) {
    let dom = document.getElementById(name);
    dom.addEventListener('click', function () {
        if (block[name]) return;
        block[name] = true;
        dom.setAttribute('disabled', '');
        request({command: name}, function (response) {
            block[name] = false;
            dom.removeAttribute('disabled');
        });
    });
}

document.addEventListener("DOMContentLoaded", function() {
    process_board();
});
setInterval(()=>{
    process_board();
},8000);