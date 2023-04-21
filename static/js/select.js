var x, i, j, l, ll, selElmnt, a, b, c;
/* Look for any elements with the class "custom-select": */
x = document.getElementsByClassName("memesui--controls--custom-select");
l = x.length;
for (i = 0; i < l; i++) {
  selElmnt = x[i].getElementsByTagName("select")[0];
  ll = selElmnt.length;
  /* For each element, create a new DIV that will act as the selected item: */
  a = document.createElement("DIV");
  a.setAttribute("class", "memesui--controls--select-selected");
  
  var selectedText = document.createTextNode(selElmnt.options[selElmnt.selectedIndex].innerHTML);
  var selectedElm = document.createElement("DIV");
  selectedElm.setAttribute("class", "memesui--controls--selected-text");
  selectedElm.appendChild(selectedText);
  a.appendChild(selectedElm);
  
  x[i].appendChild(a);
  /* For each element, create a new DIV that will contain the option list: */
  b = document.createElement("DIV");
  b.setAttribute("class", "memesui--controls--select-items memesui--controls--select-hide");
  for (j = 1; j < ll; j++) {
    /* For each option in the original select element,
    create a new DIV that will act as an option item: */
    c = document.createElement("DIV");
    c.setAttribute("class", "memesui--controls--option");
    d = document.createElement("DIV");
    d.setAttribute("class", "memesui--controls--option-text");
    
    var optionText = document.createTextNode(selElmnt.options[j].innerHTML);
    d.appendChild(optionText);
    c.appendChild(d);
    c.addEventListener("click", function(e) {
        /* When an item is clicked, update the original select box,
        and the selected item: */
        var y, i, k, s, h, sl, yl;
        s = this.parentNode.parentNode.getElementsByTagName("select")[0];
        sl = s.length;
        h = this.parentNode.previousSibling;
        for (i = 0; i < sl; i++) {
          if (s.options[i].innerHTML == this.children[0].innerHTML) {
            s.selectedIndex = i;
            var selectedText = document.createTextNode(this.children[0].innerHTML);
            var selectedElm = document.createElement("DIV");
            selectedElm.setAttribute("class", "memesui--controls--selected-text");
            selectedElm.appendChild(selectedText);
            h.innerHTML = '';
            h.appendChild(selectedElm);
            y = this.parentNode.getElementsByClassName("memesui--controls--option-selected");
            yl = y.length;
            for (k = 0; k < yl; k++) {
                y[k].setAttribute("class", "memesui--controls--option");
            }
              this.setAttribute("class", "memesui--controls--option-selected");
            break;
          }
        }
        h.click();
    });
    b.appendChild(c);
  }
  x[i].appendChild(b);
  a.addEventListener("click", function(e) {
    /* When the select box is clicked, close any other select boxes,
    and open/close the current select box: */
    e.stopPropagation();
    closeAllSelect(this);
    this.nextSibling.classList.toggle("memesui--controls--select-hide");
    this.classList.toggle("memesui--controls--select-arrow-active");
  });
}

function closeAllSelect(elmnt) {
  /* A function that will close all select boxes in the document,
  except the current select box: */
  var x, y, i, xl, yl, arrNo = [];
  x = document.getElementsByClassName("memesui--controls--select-items");
  y = document.getElementsByClassName("memesui--controls--select-selected");
  xl = x.length;
  yl = y.length;
  for (i = 0; i < yl; i++) {
    if (elmnt == y[i]) {
      arrNo.push(i)
    } else {
      y[i].classList.remove("memesui--controls--select-arrow-active");
    }
  }
  for (i = 0; i < xl; i++) {
    if (arrNo.indexOf(i)) {
      x[i].classList.add("memesui--controls--select-hide");
    }
  }
}

/* If the user clicks anywhere outside the select box,
then close all select boxes: */
document.addEventListener("click", closeAllSelect);  