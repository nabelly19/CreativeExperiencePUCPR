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
}

function filterCards() {
    const input = document.getElementById('searchInput');
    const filter = input.value.toLowerCase();
    const cards = document.getElementsByClassName('card');

    for (let i = 0; i < cards.length; i++) {
        const card = cards[i];
        const cardText = card.textContent || card.innerText;
        if (cardText.toLowerCase().indexOf(filter) > -1) {
            card.style.display = "";
        } else {
            card.style.display = "none";
        }
    }
}