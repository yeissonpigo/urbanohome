function minus_counter(quantityId) {
    var myQuantity = document.getElementById('quantity'+quantityId)
    var myValue = Number(myQuantity.value) || 0;
    if(myValue > 0)
    myQuantity.value = Number(myValue - 1);
}

function plus_counter(quantityId) {
    var myQuantity = document.getElementById('quantity'+quantityId)
    var myValue = Number(myQuantity.value) || 0;
    if(myValue < 20)
    myQuantity.value = Number(myValue + 1);
}