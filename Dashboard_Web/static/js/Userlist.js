var input_apagar = document.getElementById("validation");
var word = "APAGAR";

function request(){
    if (input_apagar.value == word){
        //quando true faz requisição
        console.log("tá podendo");
        return true;
    }

    else 
        console.log("não tá podendo");
        return false;
<<<<<<< Updated upstream
}


document.addEventListener('DOMContentLoaded', function () {
    const modals = document.querySelectorAll('.modal');
    const deleteButtons = document.querySelectorAll('.apagar');

    deleteButtons.forEach((button, index) => {
        button.addEventListener('click', function () {
            const modal = modals[index];
            const name = this.parentNode.parentNode.querySelector('.card-title').textContent.split(":")[1].trim();
            modal.querySelector('.modal-body h3').textContent = `Confirme a remoção de ${name}`;
        });
    });
});
=======
}
>>>>>>> Stashed changes
