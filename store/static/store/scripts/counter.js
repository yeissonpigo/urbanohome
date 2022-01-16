function minus_counter(quantityId) {
    var myQuantity = document.getElementById('quantity' + quantityId)
    var myValue = Number(myQuantity.value) || 0;
    if (myValue > 0) {
        myQuantity.value = Number(myValue - 1);
        button_on(quantityId);
    }
}

function plus_counter(quantityId) {
    var myQuantity = document.getElementById('quantity' + quantityId)
    var myValue = Number(myQuantity.value) || 0;
    if (myValue < 20) {
        myQuantity.value = Number(myValue + 1);
        button_on(quantityId);
    }
}

function button_on(quantityId) {
    var myButton = document.getElementById('save_cart' + quantityId)
    update_button(false, 'Guardar', myButton);
}

function update_button (disable, text, element) {
    element.disabled = disable;
    element.firstChild.innerHTML = text;
}