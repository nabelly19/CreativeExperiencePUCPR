function updateDateTime() {
  const now = new Date(); // Obter a data e hora atual

  // Formatar a data no formato dia/mês/ano
  const formattedDate = `${now.getDate()}/${now.getMonth() + 1}/${now.getFullYear()}`;

  // Formatar a hora no formato HH:mm:ss (24 horas)
  const formattedTime = `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}:${String(now.getSeconds()).padStart(2, '0')}`;

  // Atualizar o conteúdo das divs com a data e hora formatadas
  document.getElementById('data').textContent = formattedDate;
  document.getElementById('hora').textContent = formattedTime;
}

<<<<<<< Updated upstream
function action(cb, id) {
  var topic = "";
  if (id == "control"){
    topic="/Action/alerta";
  }

  var data = "";
  if (cb.checked){
    data = "1";
  }else{
    data = "0";
  }

  $.ajax({
    url: "{{url_for('publish_message')}}",
    contentType: 'application/json;charset=UTF-8',
    cache: false,
    method: 'POST',
    dataType: 'json',
    data: JSON.stringify({
        message: data,
        topic: topic
    })
  })
}


=======
>>>>>>> Stashed changes
// Atualizar a hora a cada segundo
setInterval(updateDateTime, 1000);

// Chamar a função updateTime pela primeira vez para exibir imediatamente a hora
updateDateTime();
