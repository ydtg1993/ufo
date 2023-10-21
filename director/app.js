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
    request({command:'process-board'},function (response) {
        if(response.code !== 0){
            alert(response.message);
            return;
        }
        let process_dom = document.querySelector('#process-board>div:first-child');
        let html = '';
        for (const d in response.data.process){
            let panel = `<div class="box"><div class="process"><span class="letters">{message}</span><i class="tag {type}"></i></div></div>`;
            panel = panel.replace("{message}", d + ' --- ' + response.data.process[d]['time']);
            let type = 'green';
            if(!response.data.process[d]['live']){
                type = 'red square';
            }
            panel = panel.replace("{type}", d + ' --- ' + type);
            html += panel
        }
        process_dom.innerHTML = html;

        let process_stop_dom = document.querySelector('#process-board>div:nth-child(2)');
        html = '';
        for (let i=1;i<=response.data.stop_signal.full_num;i++){
            if(i > response.data.stop_signal.num){
                  html += '<i class="tag red square" style="margin-right: 3px"></i>';
            }else{
                 html += '<i class="tag green square" style="margin-right: 3px"></i>';
            }
        }
        process_stop_dom.innerHTML = html;
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
},80000);