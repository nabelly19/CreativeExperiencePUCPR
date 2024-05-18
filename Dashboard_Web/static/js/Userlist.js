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