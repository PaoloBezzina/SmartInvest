let cardContainer;

let createTaskCard = (walletListing) => {
    let rowEntry = document.createElement("tr");

    let code = document.createElement("th");
    code.scope = "row";
    code.innerText = walletListing.code;

    let title = document.createElement("td");
    title.innerText = walletListing.title;

    let price = document.createElement("td");
    price.innerText = "€" + walletListing.price;

    let units = document.createElement("td");
    units.innerText = walletListing.units;

    let value = document.createElement("td");
    value.innerText = "€" + walletListing.value;

    let type = document.createElement("td");
    type.innerText = walletListing.type;

    rowEntry.appendChild(code);
    rowEntry.appendChild(title);
    rowEntry.appendChild(price);
    rowEntry.appendChild(units);
    rowEntry.appendChild(value);
    rowEntry.appendChild(type);
    cardContainer.appendChild(rowEntry);
};

/* "json/walletListings.json" */
let getCryptoListings = () => {
    return new Promise((resolve, reject) => {
        $.getJSON(filePath, (data) => {
            resolve(data);
        }).fail((error) => {
            reject(error);
        });
    });
};

var walletList = [];

var filePath;
/* try to read file from element, otherwise read from path */
if (document.getElementById("wallet-script").getAttribute("data-file-path")) {
    filePath = document
        .getElementById("wallet-script")
        .getAttribute("data-file-path");
} else {
    filePath = "json/walletListings.json";
}

let initListOfCrypto = () => {
    /* if walletList is not initialised, getCryptoListings */
    if (walletList.length == 0) {
        getCryptoListings()
            .then((data) => {
                walletList = data;
                console.log(walletList);

                if (cardContainer) {
                    document
                        .getElementById("wallet-table-body")
                        .replaceWith(cardContainer);
                    return;
                }

                cardContainer = document.getElementById("wallet-table-body");

                walletList.forEach((walletListing) => {
                    createTaskCard(walletListing);
                });
            })
            .catch((error) => {
                console.log(error);
            });
    }
};

window.onload = function() {
    initListOfCrypto();
};