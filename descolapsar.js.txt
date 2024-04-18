var elementos = document.getElementsByClassName("mbl-OpenBetItem_Header mbl-OpenBetItem_HeaderTitle ");
console.log(elementos.length);
for (let elem of elementos) {
    elem.click();
}
var container = document.getElementsByClassName("mbl-BetItemsContainer_BetItemsContainer ");
console.log(container[0]);
