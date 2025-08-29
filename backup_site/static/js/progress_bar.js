function showProgressBar(taskId, labelText, progressUrl) {
    const container = document.getElementById('progress-bar-container');
    const bar = document.getElementById('progress-bar');
    const label = document.getElementById('progress-bar-label');
    const status = document.getElementById('progress-bar-status');
    if (!container || !bar || !label || !status) return;
    container.style.display = 'block';
    label.textContent = labelText || 'Processando...';
    bar.style.width = '0%';
    status.textContent = '';

    function poll() {
        fetch(progressUrl.replace('TASK_ID', taskId))
            .then(response => response.json())
            .then(data => {
                let pct = data.progress || 0;
                bar.style.width = pct + '%';
                if (data.state === 'SUCCESS' || data.status === 'ok') {
                    bar.style.width = '100%';
                    status.textContent = 'Concluído com sucesso!';
                    setTimeout(() => { container.style.display = 'none'; }, 2000);
                } else if (data.state === 'FAILURE' || data.status === 'erro') {
                    status.textContent = 'Erro ao processar.';
                } else {
                    status.textContent = 'Progresso: ' + pct + '%';
                    setTimeout(poll, 1000);
                }
            })
            .catch(() => {
                status.textContent = 'Erro ao consultar progresso.';
            });
    }
    poll();
} 