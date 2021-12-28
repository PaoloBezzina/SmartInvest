function randomDate(start, end) {
    return new Date(start.getTime() + Math.random() * (end.getTime() - start.getTime()));
}

let dateDisp = document.getElementById("date-generated");

var date = randomDate(new Date(2019, 0, 1), new Date(2021, 10, 31));
dateDisp.innerHTML = date.toLocaleDateString();
console.log(date);

window.onload = function() {
    var date = randomDate(new Date(2019, 0, 1), new Date(2021, 10, 31));
    dateDisp.innerHTML = date.toLocaleDateString();
    console.log(date);
}