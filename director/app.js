function process_board() {
    _component.request({
        url: window.location.href,method:'POST', data: {command: 'process-board'}, callback: function (response) {
            if (response.code !== 0) {
                alert(response.message);
                return;
            }
            let html = '';
            let current_task_dom = document.querySelector('#current-task-board');
            response.data.current_task.forEach(function (item) {
                html += `<button class="dlp-button dlp-button-blue" disabled>${item}</button>`;
            });
            current_task_dom.innerHTML = html;

            html = '';
            let process_dom = document.querySelector('#process-board>div:first-child');
            for (const d in response.data.process) {
                let panel = `<div class="box"><div class="process"><span class="letters">{message}</span><i class="tag {type}"></i></div></div>`;
                panel = panel.replace("{message}", d + ' --- ' + response.data.process[d]['time']);
                let type = 'green';
                if (!response.data.process[d]['live']) {
                    type = 'red square';
                }
                panel = panel.replace("{type}", d + ' --- ' + type);
                html += panel;
            }
            process_dom.innerHTML = html;

            let process_stop_dom = document.querySelector('#process-board>div:nth-child(2)');
            html = '';
            for (let i = 1; i <= response.data.stop_signal.full_num; i++) {
                if (i > response.data.stop_signal.num) {
                    html += '<i class="tag red square" style="margin-right: 3px"></i>';
                } else {
                    html += '<i class="tag green square" style="margin-right: 3px"></i>';
                }
            }
            process_stop_dom.innerHTML = html;

            let process_task_menu_dom = document.querySelector('#task-board>div:first-child');
            process_task_menu_dom.innerHTML = '';
            for(let i in response.data.process_cache_conf){
                let menu_dom = document.createElement('button');
                menu_dom.className = 'dlp-button dlp-button-green';
                menu_dom.textContent = response.data.process_cache_conf[i]['name'];
                menu_dom.addEventListener('click',()=>{
                    if (response.data.process_cache_conf[i]['type'] === 'queue'){
                        taskQueueEvent(response.data.process_cache_conf[i]['key'],response.data.process_cache_conf[i]['type'])
                    }else{

                    }
                });
                process_task_menu_dom.insertAdjacentElement('afterbegin',menu_dom)
            }
        }
    });

    function taskQueueEvent(cache,type) {
        if (block.process_cache) return;
        block.process_cache = true;
         _component.request({url: window.location.href,method:'POST', data: {command: 'process_cache',cache:cache,type:type},callback:function (response) {
            block.process_cache = false;
            let dom = document.querySelector('#task-board>div:nth-child(2)');

        }});
    }
}

let block = {command_stop: false, command_reset_comic: false, command_reset_chapter: false,process_cache:false};

function buttonEvent(name) {
    let dom = document.getElementById(name);
    dom.addEventListener('click', function () {
        if (block[name]) return;
        block[name] = true;
        dom.setAttribute('disabled', '');
        _component.request({url: window.location.href,method:'POST', data: {command: name},callback:function (response) {
            block[name] = false;
            dom.removeAttribute('disabled');
        }});
    });
}

document.addEventListener("DOMContentLoaded", function () {
    process_board();
});
setInterval(() => {
    process_board();
}, 80000);