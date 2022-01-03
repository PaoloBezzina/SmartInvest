let tableContainer;

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
    tableContainer.appendChild(rowEntry);
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

let initList = () => {
    /* if walletList is not initialised, getCryptoListings */
    if (walletList.length == 0) {
        getCryptoListings()
            .then((data) => {
                walletList = data;

                if (tableContainer) {
                    document
                        .getElementById("wallet-table-body")
                        .replaceWith(tableContainer);
                    return;
                }

                tableContainer = document.getElementById("wallet-table-body");

                walletList.forEach((walletListing) => {
                    createTaskCard(walletListing);
                });
            })
            .catch((error) => {
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
    initList();
    getMoney();
};