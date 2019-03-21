function disableElements(id){
    var i;
    for (i in id){
        document.getElementById(id[i]).disabled = true;
    }
}
function enableElements(id){
    var i;
    for (i in id){
        document.getElementById(id[i]).disabled = false;
    }
}