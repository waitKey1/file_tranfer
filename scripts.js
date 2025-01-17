// 假设后端API的URL是以下地址
const API_URL = 'http://sztuwork.sligenai.cn/funiapi';

// 加载文件列表
function loadFileList() {
    fetch(`${API_URL}/files`)
        .then(response => response.json())
        .then(files => {
            const fileList = document.getElementById('files');
            fileList.innerHTML = '';
            files.forEach(file => {
                const li = document.createElement('li');
                li.textContent = file.name;
                const downloadBtn = document.createElement('button');
                downloadBtn.textContent = '下载';
                downloadBtn.onclick = () => downloadFile(file.name);
                li.appendChild(downloadBtn);
                fileList.appendChild(li);
            });
        });
}

// 上传文件
function uploadFiles() {
    const input = document.getElementById('file-input');
    const data = new FormData();
    for (const file of input.files) {
        data.append('files', file);
    }

    fetch(`${API_URL}/upload`, {
        method: 'POST',
        body: data
    })
    .then(response => response.json())
    .then(result => {
        console.log('Success:', result);
        loadFileList(); // 重新加载文件列表
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// 下载文件
function downloadFile(filename) {
    window.open(`${API_URL}/download/${filename}`);
}

// 页面加载时获取文件列表
window.onload = loadFileList;
