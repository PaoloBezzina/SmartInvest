let cardContainer;

let createTaskCard = (cryptoListing) => {
    let card = document.createElement("div");
    card.className = "card col-sm-5 cursor-pointer";

    let cardBody = document.createElement("div");
    cardBody.className = "card-body";

    let code = document.createElement("h5");
    code.className = "card-title";
    code.innerHTML = cryptoListing.code;

    let title = document.createElement("h5");
    title.className = "card-title";
    title.innerText = cryptoListing.title;

    let value = document.createElement("p");
    value.className = "card-text";
    value.innerText = "Value: €" + cryptoListing.value;

    let info = document.createElement("a");
    info.className = "btn btn-primary";
    info.innerText = "Info";
    info.onclick = function() {
        window.open(cryptoListing.info, "_blank");
    };

    let form = document.createElement("form");
    form.action = cryptoListing.href;
    form.method = "post";

    let button = document.createElement("button");
    button.className = "btn btn-primary";
    button.type = "submit";
    button.name = "coin-code";
    button.value = cryptoListing.code;
    button.innerText = "Simulate";

    button.href = cryptoListing.href;

    form.appendChild(button);
    cardBody.appendChild(code);
    cardBody.appendChild(title);
    cardBody.appendChild(value);
    cardBody.appendChild(info);
    cardBody.appendChild(form);
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

window.onload = function() {
    initListOfCrypto();
};