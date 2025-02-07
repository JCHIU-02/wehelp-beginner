//toggle-menu
var menuToggle = document.getElementById('menu-toggle');
var mobileMenu = document.getElementById('mobile-menu');
var closeMenu = document.getElementById('close-menu');
menuToggle.addEventListener('click', function() {
    mobileMenu.classList.add('active'); //在mobileMenu標籤物件加上class="active"，並在CSS style裡添加.mobile-menu.active的樣式，HTML不動-->隱藏的手機menu被推出來(right=0)
});
closeMenu.addEventListener('click', function() {
    mobileMenu.classList.remove('active');//在mobileMenu標籤物件移除class="active"
});


//rendering
const URL = 'https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1';
// 抓取資料並渲染
fetch(URL)
.then(response => response.json()) // 將回應轉為 JSON 格式
.then(data => {
    renderData(data.data.results); // 調用渲染函式
})
.catch(error => {
  console.error(error); // 處理錯誤
});

function renderData(spots) {

  const bottomColumn = document.getElementById('bottom-content') //要把 bottom-content 這個 DOM 傳給 bottomColumn 的意義，是不是在Bottom Column裡建立的 div、資料才能渲染進原本的靜態網頁 
  const topColumn = document.getElementById('top-content')

  for(let i=0; i<3; i++){
      
    //create promotion block
    const pContainer = document.createElement('div')
    const pImgBox = document.createElement('div')
    const pImg = document.createElement('img')
    const pText = document.createElement('div')

    //add class
    pContainer.classList.add('promotion')
    pImgBox.classList.add('imgbox')
    pText.classList.add('word')

    //add to parent node
    pImgBox.appendChild(pImg)
    pContainer.appendChild(pImgBox)
    pContainer.appendChild(pText)
    topColumn.appendChild(pContainer)

    pText.innerText = spots[i].stitle

    let img = spots[i].filelist
    let rule = new RegExp('jpg', 'i');
    let theJpg = img.match(rule);
    let jpgIndex = img.indexOf(theJpg[0]);
    let firstImg = img.slice(0, jpgIndex + 3);

    pImg.src = firstImg
  } 

  for(let i=3; i<13; i++){

    if(i % 5 === 3){

    //creat largebox block
    const bContainer = document.createElement('div')
    const bImg = document.createElement('img')
    const bTextBlock = document.createElement('div')
    const bText = document.createElement('p')
    const bStarIcon = document.createElement('div')
    const bStarImg = document.createElement('img')
    bottomColumn.appendChild(bContainer)

    bStarIcon.appendChild(bStarImg)
    bContainer.appendChild(bStarIcon)
    bContainer.appendChild(bImg)
    bTextBlock.appendChild(bText)
    bContainer.appendChild(bTextBlock)
    bottomColumn.appendChild(bContainer)
    
    bContainer.classList.add('large-box')
    bTextBlock.classList.add('text-block-large')
    bStarIcon.classList.add('star-container')
    bText.classList.add('text-in-block')

    bText.innerText = spots[i].stitle

    let img = spots[i].filelist
    let rule = new RegExp('jpg', 'i');
    let theJpg = img.match(rule);
    let jpgIndex = img.indexOf(theJpg[0]);
    let firstImg = img.slice(0, jpgIndex + 3);
      
    bImg.src = firstImg
    bStarImg.src = "star.png"
    bText.innerText = spots[i].stitle

    }

    else{
      const sContainer = document.createElement('div')
      const sImg = document.createElement('img')
      const sTextBlock = document.createElement('div')
      const sText = document.createElement('p')
      const sStarIcon = document.createElement('div')
      const sStarImg = document.createElement('img')

      sStarIcon.appendChild(sStarImg)
      sContainer.appendChild(sStarIcon)
      sContainer.appendChild(sImg)
      sTextBlock.appendChild(sText)
      sContainer.appendChild(sTextBlock)
      bottomColumn.appendChild(sContainer)
      
      sContainer.classList.add('small-box')
      sTextBlock.classList.add('text-block-small')
      sStarIcon.classList.add('star-container')
      sText.classList.add('text-in-block')

      let img = spots[i].filelist
      let rule = new RegExp('jpg', 'i');
      let theJpg = img.match(rule);
      let jpgIndex = img.indexOf(theJpg[0]);
      let firstImg = img.slice(0, jpgIndex + 3);
      
      sImg.src = firstImg
      sStarImg.src = "star.png"
      sText.innerText = spots[i].stitle
    }     
  }
}