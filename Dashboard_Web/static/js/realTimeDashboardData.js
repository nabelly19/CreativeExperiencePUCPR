var $SCRIPT_ROOT = {{ request.script_root|tojson|safe }};
var intervalID = setInterval(update_values,5000);

  function update_values() {
        $.getJSON($SCRIPT_ROOT + '/realTimeData',

      function(data) {
        var temperatura = data.Temperatura;
        var umidade = data.Umidade;
        var mensagemDeAlerta = data["Mensagem de alerta"];
        var nivelDaAgua = data["Nível da água"];
        var statusDoAlarme = data["Status do alarme"];
        
        // Atualizando elementos HTML com os valores
        $('#temperatura').text(temperatura);
        $('#umidade').text(umidade);
        $('#mensagemDeAlerta').text(mensagemDeAlerta);
        $('#nivelDaAgua').text(nivelDaAgua);
        $('#statusDoAlarme').text(statusDoAlarme);
      });
      
    };