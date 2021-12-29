let cardContainer;

let createTaskCard = (stocksListing) => {
    let card = document.createElement("div");
    card.className = "card col-sm-5 cursor-pointer align-self-center d-flex justify-content-between";

    let cardBody = document.createElement("div");
    cardBody.className = "card-body";

    let code = document.createElement("h3");
    code.className = "card-title col-sm-2";
    code.style.marginTop = "10px";
    code.style.marginBottom = "20px";
    code.innerHTML = stocksListing.code;

    let title = document.createElement("h4");
    title.className = "card-title col-sm-4 text-left";
    title.innerText = stocksListing.title;

    let info = document.createElement("a");
    info.className = "btn btn-primary col-sm-offset-3 col-sm-2";
    info.innerText = "Info";
    info.onclick = function() {
        window.open(stocksListing.info, "_blank");
    };

    let value = document.createElement("p");
    value.className = "card-text col-sm-12";
    value.innerText = "Value: €" + stocksListing.value;

    let formBody = document.createElement("div");
    cardBody.className = "card-body ml-auto";

    let form = document.createElement("form");
    form.action = stocksListing.href;
    form.method = "post";

    let amountText = document.createElement("p");
    amountText.className = "col-sm-3 float-right";
    amountText.innerText = "Amount (€): ";

    let button = document.createElement("button");
    button.className = "btn btn-primary col-sm-offset-3 col-sm-2 float-right";
    button.type = "submit";
    button.name = "code";
    button.value = stocksListing.code;
    button.innerText = "Purchase";
    button.href = stocksListing.href;

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
    priceSend.value = stocksListing.value;

    let typeSend = document.createElement("input");
    typeSend.className = "hidden";
    typeSend.type = "hidden";
    typeSend.style.display = "none";
    typeSend.name = "type";
    typeSend.value = "Stocks";

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

/* "json/stocksListings.json" */
let getStocksListings = () => {
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

let initListOfStocks = () => {
    /* if stocksList is not initialised, getStocksListings */
    if (stocksList.length == 0) {
        getStocksListings()
            .then((data) => {

                stocksList = data;

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
    initListOfStocks();
};