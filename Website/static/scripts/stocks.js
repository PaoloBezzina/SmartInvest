let cardContainer;

let createTaskCard = (stocksListing) => {
    let card = document.createElement("div");
    card.className = "card col-sm-5 cursor-pointer";

    let cardBody = document.createElement("div");
    cardBody.className = "card-body";

    let code = document.createElement("h5");
    code.className = "card-title";
    code.innerHTML = stocksListing.code;

    let title = document.createElement("h5");
    title.className = "card-title";
    title.innerText = stocksListing.title;

    let value = document.createElement("p");
    value.className = "card-text";
    value.innerText = "Value: €" + stocksListing.value;

    let button = document.createElement("a");
    button.className = "btn btn-primary";
    button.innerText = "Simulate";
    button.href = stocksListing.href;

    cardBody.appendChild(code);
    cardBody.appendChild(title);
    cardBody.appendChild(value);
    cardBody.appendChild(button);
    card.appendChild(cardBody);
    cardContainer.appendChild(card);
};

/* "json/stocksListings.json" */
let getCryptoListings = () => {
    return new Promise((resolve, reject) => {
        $.getJSON(filePath, (data) => {
            resolve(data);
        }).fail((error) => {
            reject(error);
        });
    });
};

var stocksList = [];

var filePath;
/* try to read file from element, otherwise read from path */
if (document.getElementById("stocks-script").getAttribute("data-file-path")) {
    filePath = document.getElementById("stocks-script").getAttribute("data-file-path");
} else {
    filePath = "json/stocksListings.json";
}

let initListOfCrypto = () => {
    /* if stocksList is not initialised, getCryptoListings */
    if (stocksList.length == 0) {
        getCryptoListings()
            .then((data) => {

                stocksList = data;
                console.log(stocksList);

                if (cardContainer) {
                    document
                        .getElementById("stocks-card-container")
                        .replaceWith(cardContainer);
                    return;
                }

                cardContainer = document.getElementById("stocks-card-container");

                stocksList.forEach((stocksListing) => {
                    createTaskCard(stocksListing);
                });
            }).catch((error) => {
                console.log(error);
            });
    }
};

window.onload = function() {
    initListOfCrypto();
};