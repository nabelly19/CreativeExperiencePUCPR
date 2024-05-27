// Função para habilitar e desabilitar campos de seleção
function toggleSelects() {
    const deviceSelect = document.getElementById('deviceSelect');
    const topicSelect = document.getElementById('topicSelect');

    if (deviceSelect.value !== 'Escolher dispositivo') {
        topicSelect.disabled = true;
        topicSelect.classList.add('disabled-select', 'blocked-pointer');
    } else {
        topicSelect.disabled = false;
        topicSelect.classList.remove('disabled-select', 'blocked-pointer');
    }

    if (topicSelect.value !== 'Escolher tópico') {
        deviceSelect.disabled = true;
        deviceSelect.classList.add('disabled-select', 'blocked-pointer');
    } else {
        deviceSelect.disabled = false;
        deviceSelect.classList.remove('disabled-select', 'blocked-pointer');
    }
}

// Adicionar event listeners aos campos de seleção especificados
window.onload = function() {
    const deviceSelect = document.getElementById('deviceSelect');
    const topicSelect = document.getElementById('topicSelect');

    deviceSelect.addEventListener('change', toggleSelects);
    topicSelect.addEventListener('change', toggleSelects);
}
