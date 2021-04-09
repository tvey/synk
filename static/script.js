function copyToClipboard(elem, button = false, copied = false) {
  let textElem = elem.previousElementSibling;
  let range = document.createRange();
  range.selectNode(textElem);
  window.getSelection().removeAllRanges(); 
  window.getSelection().addRange(range); 
  document.execCommand("copy");
  window.getSelection().removeAllRanges();

  if(button === true) {
    elem.innerHTML = "Copied!";
    elem.style.backgroundColor = "#eb00eb";
  } else {
    textElem.style.color = "#e73c7e";
    elem.style.color = "#2388d5";
    if (copied === true) {
      let copiedAlert = document.getElementById("copied");
      if (document.contains(copiedAlert)) {
        copiedAlert.remove();
      }
      let newCopiedAlert = document.createElement("div");
      newCopiedAlert.id = 'copied';
      newCopiedAlert.innerHTML = " Copied!";
      newCopiedAlert.style.color = "#2388d5";
      elem.after(newCopiedAlert);
    }
  }
}

function prevElem(elem) {
  do {
    elem = elem.previousSibling;
  } while (elem && elem.nodeType != 1);
  return elem;                
}

function togglePreviousSibling(elem) {
  let previousElem = prevElem(elem);

  if (previousElem.style.display === 'inline-block') {
    previousElem.style.display ='none'; 
    elem.innerHTML = "Show";
  }
  else { 
    previousElem.style.display='inline-block';
    elem.innerHTML = "Hide";
  }
}

let resultInput = document.querySelector("#result #id_url")
if (resultInput) { 
  resultInput.addEventListener('click', () => {
    resultInput.select();
  })
}

let mainHeading = document.getElementById('main-heading');
if (mainHeading) {
  mainHeading.addEventListener('animationend', () => {
    mainHeading.classList.remove('animated');
  });
  mainHeading.addEventListener('mouseover', () => {
    mainHeading.classList.add('animated')
  }) 
}


let codeInput = document.getElementById("id_code");
if (codeInput) {
  let codeLabel = codeInput.previousElementSibling;
  console.log(codeLabel);
  let copied = document.createElement("div");
}


