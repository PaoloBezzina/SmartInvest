let evaluationTableContainer;

let createEvaluationTable = (evaluationListing) => {
    let evaluationRowEntry = document.createElement("tr");

    let code = document.createElement("th");
    code.scope = "row";
    code.innerText = evaluationListing.code;

    let pastValue = document.createElement("td");
    pastValue.innerText = "€" + Math.round(evaluationListing.pastValue * 100) / 100;

    let currentValue = document.createElement("td");
    currentValue.innerText = "€" + Math.round(evaluationListing.currentValue * 100) / 100;

    let pastPrice = document.createElement("td");
    pastPrice.innerText = "€" + Math.round(evaluationListing.pastPrice * 100) / 100;

    let currentPrice = document.createElement("td");
    currentPrice.innerText = "€" + Math.round(evaluationListing.currentPrice * 100) / 100;

    let roiVal = document.createElement("td");
    roiVal.innerText = "€" + Math.round(evaluationListing.roiVal * 100) / 100;
    if (evaluationListing.roiVal < 0) {
        roiVal.style.color = "red";
    } else {
        roiVal.style.color = "green";
    }

    let roiPerc = document.createElement("td");
    roiPerc.innerText = Math.round(evaluationListing.roiPerc * 100) / 100 + "%";
    if (evaluationListing.roiPerc < 0) {
        roiPerc.style.color = "red";
    } else {
        roiPerc.style.color = "green";
    }

    evaluationRowEntry.appendChild(code);
    evaluationRowEntry.appendChild(pastValue);
    evaluationRowEntry.appendChild(currentValue);
    evaluationRowEntry.appendChild(pastPrice);
    evaluationRowEntry.appendChild(currentPrice);
    evaluationRowEntry.appendChild(roiVal);
    evaluationRowEntry.appendChild(roiPerc);
    evaluationTableContainer.appendChild(evaluationRowEntry);
};

/* "json/evaluationListings.json" */
let getEvaluationListings = () => {
    return new Promise((resolve, reject) => {
        $.getJSON(evaluationFilePath, (data) => {
            resolve(data);
        }).fail((error) => {
            reject(error);
        });
    });
};

var evaluationList = [];

var evaluationFilePath;
/* try to read file from element, otherwise read from path */
if (document.getElementById("evaluation-script").getAttribute("data-file-path")) {
    evaluationFilePath = document
        .getElementById("evaluation-script")
        .getAttribute("data-file-path");
} else {
    evaluationFilePath = "json/evaluation.json";
}

let initEvaluationList = () => {
    /* if evaluationList is not initialised, getEvaluationListings */
    if (evaluationList.length == 0) {
        getEvaluationListings()
            .then((data) => {
                evaluationList = data;

                if (evaluationTableContainer) {
                    document
                        .getElementById("evaluation-table-body")
                        .replaceWith(evaluationTableContainer);
                    return;
                }

                evaluationTableContainer = document.getElementById("evaluation-table-body");

                evaluationList.forEach((evaluationListing) => {
                    createEvaluationTable(evaluationListing);
                });
            })
            .catch((error) => {
                console.log(error);
            });
    }
};

/* ----------------------------------------------------------------------------------------------------------------- */
let getTotalEvaluationListings = () => {
    return new Promise((resolve, reject) => {
        $.getJSON(totalEvaluationFilePath, (data) => {
            resolve(data);
        }).fail((error) => {
            reject(error);
        });
    });
};

var totalEvaluationList = [];

let initTotalEvaluationList = () => {
    /* if totalEvaluationList is not initialised, getTotalEvaluationListings */
    if (totalEvaluationList.length == 0) {
        getTotalEvaluationListings()
            .then((data) => {
                totalEvaluationList = data;

                /* change document.getElementById("return-on-investments-money").innerText to mathc the value of totalROIVal from json file */
                document.getElementById("return-on-investments-money").innerText = "€" + Math.round(totalEvaluationList.totalROIVal * 100) / 100;
                if (totalEvaluationList.totalROIVal < 0) {
                    document.getElementById("return-on-investments-money").style.color = "red";
                } else {
                    document.getElementById("return-on-investments-money").style.color = "green";
                }

                /* change document.getElementById("return-on-investments-money").innerText to mathc the value of totalROIVal from json file */
                document.getElementById("total-value-simulate").innerText = "€" + Math.round(totalEvaluationList.currentValue * 100) / 100;

                document.getElementById("evaluation-info").style.visibility = "visible";

            })
            .catch((error) => {
                console.log(error);
            });
    }
};

var totalEvaluationFilePath;
/* try to read file from element, otherwise read from path */
if (document.getElementById("evaluation-script").getAttribute("data-total-file-path")) {
    totalEvaluationFilePath = document
        .getElementById("evaluation-script")
        .getAttribute("data-total-file-path");
} else {
    totalEvaluationFilePath = "json/total_evaluation.json";
}

function SubmitForm() {

    document.forms['evaluate-form'].action = '/evaluate';
    document.forms['evaluate-form'].submit();

    /* wait 2 seconds */
    setTimeout(function() {
        initEvaluationList();
        initTotalEvaluationList();
    }, 5000);

}