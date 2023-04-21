

const tabHeaderBtns = document.querySelectorAll('[id^="header-button"]');
const tabs = document.querySelectorAll('[class^="content--section"]');
tabHeaderBtns.forEach(clickOnTab);

function clickOnTab(item){
  item.addEventListener("click", function(){
    let curBtn = item;
    let tabID = curBtn.getAttribute("data-tab");
    let curTab = document.querySelector(tabID);

    if ( ! curBtn.classList.contains('active')){
      tabHeaderBtns.forEach(function(item){
        item.classList.remove('active');
      })

      tabs.forEach(function(item){
          item.classList.replace('content--section--active','content--section' );
      })

      curBtn.classList.add('active');
      curTab.classList.replace('content--section', 'content--section--active');
      checkScrollbar();
    }
  });
}

document.querySelector('#header-button-editor').click();
