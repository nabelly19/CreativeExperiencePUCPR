setInterval(function() {
  fetch('/realTimeData').then(
      response => response.json()
  ).then(
      data => {
          document.getElementById('temperatura').textContent = data.Temperatura + 'ºC';
          document.getElementById('umidade').textContent = data.Umidade + '%';
          document.getElementById('mensagemDeAlerta').textContent = data["Mensagem de alerta"];
          document.getElementById('nivelDaAgua').textContent = data["Nível da água"];
          document.getElementById('statusDoAlarme').textContent = data["Status do alarme"];
      }
  );
}, 5000);