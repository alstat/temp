function autoResizeDiv() {
    document.getElementById("div_main_inputs").style.height = window.innerHeight +"px";
}
window.onresize = autoResizeDiv;
autoResizeDiv();