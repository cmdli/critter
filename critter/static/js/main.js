console.log("Hello from main.js!");
var form = document.querySelector("form");
console.log(form);
function formSubmit(event) {
    console.log("Submitted: " + form.elements[0].value);
    let item = document.createElement("p");
    var text = document.getElementById("item-text");
    item.innerText = text.value;
    document.getElementById("item-list").appendChild(item);
    text.value = "";
    event.preventDefault();
}


