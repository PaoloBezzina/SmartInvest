let cardContainer;

let createTaskCard = (cryptoListing) => {
    let card = document.createElement("div");
    card.className = "card col-sm-5 cursor-pointer align-self-center d-flex justify-content-between";

    let cardBody = document.createElement("div");
    cardBody.className = "card-body";

    let code = document.createElement("h3");
    code.className = "card-title col-sm-2";
    code.style.marginTop = "10px";
    code.style.marginBottom = "20px";
    code.innerHTML = cryptoListing.code;

    let title = document.createElement("h4");
    title.className = "card-title col-sm-4 text-left";
    title.innerText = cryptoListing.title;

    let info = document.createElement("a");
    info.className = "btn btn-primary col-sm-offset-3 col-sm-2";
    info.innerText = "Info";
    info.onclick = function() {
        window.open(cryptoListing.info, "_blank");
    };

    let value = document.createElement("p");
    value.className = "card-text col-sm-12";
    value.innerText = "Value: €" + cryptoListing.value;

    let formBody = document.createElement("div");
    cardBody.className = "card-body ml-auto";

    let form = document.createElement("form");
    form.action = cryptoListing.href;
    form.method = "post";

    let amountText = document.createElement("p");
    amountText.className = "col-sm-3 float-right";
    amountText.innerText = "Amount (€): ";

    let button = document.createElement("button");
    button.className = "btn btn-primary col-sm-offset-3 col-sm-2 float-right";
    button.type = "submit";
    button.name = "code";
    button.value = cryptoListing.code;
    button.innerText = "Purchase";
    button.href = cryptoListing.href;

    let amount = document.createElement("input");
    amount.id = "amountInput";
    amount.className = "col-sm-3 float-left";
    amount.type = "number";
    amount.name = "amount-purchased";
    amount.value = "0";
    amount.min = "1";
    amount.max = "5000";
    getMoney();

    let priceSend = document.createElement("input");
    priceSend.className = "hidden";
    priceSend.type = "hidden";
    priceSend.style.display = "none";
    priceSend.name = "price";
    priceSend.value = cryptoListing.value;

    let typeSend = document.createElement("input");
    typeSend.className = "hidden";
    typeSend.type = "hidden";
    typeSend.style.display = "none";
    typeSend.name = "type";
    typeSend.value = "Crypto";

    form.appendChild(amountText);
    form.appendChild(amount);
    form.appendChild(button);
    form.appendChild(priceSend);
    form.appendChild(typeSend);

    formBody.appendChild(form);

    cardBody.appendChild(code);
    cardBody.appendChild(title);
    cardBody.appendChild(info);
    cardBody.appendChild(value);
    cardBody.appendChild(formBody);

    card.appendChild(cardBody);
    cardContainer.appendChild(card);
};

/* "json/cryptoListings.json" */
let getCryptoListings = () => {
    return new Promise((resolve, reject) => {
        $.getJSON(filePath, (data) => {
            resolve(data);
        }).fail((error) => {
            reject(error);
        });
    });
};

var cryptoList = [];

var filePath;
/* try to read file from element, otherwise read from path */
if (document.getElementById("crypto-script").getAttribute("data-file-path")) {
    filePath = document.getElementById("crypto-script").getAttribute("data-file-path");
} else {
    filePath = "json/cryptoListings.json";
}

let initListOfCrypto = () => {
    /* if cryptoList is not initialised, getCryptoListings */
    if (cryptoList.length == 0) {
        getCryptoListings()
            .then((data) => {

                cryptoList = data;

                if (cardContainer) {
                    document
                        .getElementById("crypto-card-container")
                        .replaceWith(cardContainer);
                    return;
                }

                cardContainer = document.getElementById("crypto-card-container");

                cryptoList.forEach((cryptoListing) => {
                    createTaskCard(cryptoListing);
                });
            }).catch((error) => {
                console.log(error);
            });
    }
};

function getMoney() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById("money-in-wallet").innerHTML = "€" + this.responseText;
            /* find all elements with id amountInput */
            document.querySelectorAll("#amountInput").forEach((element) => {
                element.max = this.responseText;
            });
        }
    };
    xhttp.open("GET", "/get-money/", true);
    xhttp.send();
}

window.onload = function() {
    initListOfCrypto();
};