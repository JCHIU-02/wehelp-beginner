//Task 1
function findAndPrint(messages, currentStation){

  const friendLoc = Object.values(msgShort); 
  const distArr = [];

  for(i = 0; i < friendLoc.length; i++){
    const currentIndex = mainLine.indexOf(currentStation); 
    const friendIndex = mainLine.indexOf(friendLoc[i]);

    if(mainLine.includes(currentStation) && mainLine.includes(friendLoc[i])){
      distArr.push(Math.abs(currentIndex - friendIndex));    
    } 
    else if(currentStation == "Xiaobitan" && friendLoc[i] == "Xiaobitan"){
      distArr.push(0);
    }
    else if(currentStation == "Xiaobitan"){
      distArr.push(Math.abs(friendIndex - mainLine.indexOf("Qizhang")) + 1);
    }
    else{
      distArr.push(Math.abs(currentIndex - mainLine.indexOf("Qizhang")) + 1);
    }
  }
    const nearest = distArr.reduce(function (min, dist) {
      if(min < dist){
        return min;
      } 
      else{
        return dist;
      }
    })

  const indexOfFriend = distArr.indexOf(nearest);
  const nearestFriend = Object.keys(msgShort)[indexOfFriend];
  console.log(nearestFriend);

}
  

const mainLine = [
  "Songshan",
  "Nanjing Sanmin",
  "Taipei Arena",
  "Nanjing Fuxing",
  "Songjiang Nanjing",
  "Zhongshan",
  "Beimen",
  "Ximen",
  "Xiaonanmen",
  "Chiang Kai-Shek Memorial Hall",
  "Guting",
  "Taipower Building",
  "Gongguan",
  "Wanlong",
  "Jingmei",
  "Dapinglin",
  "Qizhang",
  "Xindian City Hall",
  "Xindian"
]

const msgShort={
  "Bob":"Ximen",
  "Mary":"Jingmei",
  "Copper":"Taipei Arena",
  "Leslie":"Xiaobitan",
  "Vivian":"Xindian"
}

const messages={
"Bob":"I'm at Ximen MRT station.",
"Mary":"I have a drink near Jingmei MRT station.",
"Copper":"I just saw a concert at Taipei Arena.",
"Leslie":"I'm at home near Xiaobitan station.",
"Vivian":"I'm at Xindian station waiting for you."};

findAndPrint(messages, "Wanlong"); // print Mary
findAndPrint(messages, "Songshan"); // print Copper
findAndPrint(messages, "Qizhang"); // print Leslie
findAndPrint(messages, "Ximen"); // print Bob
findAndPrint(messages, "Xindian City Hall"); // print Vivian


//Task 2
const timeSlot = {
  "John": Array.from({ length: 24 }, (_, i) => i),
  "Bob": Array.from({ length: 24 }, (_, i) => i),
  "Jenny": Array.from({ length: 24 }, (_, i) => i)
};

function book(consultants, hour, duration, criteria){
  const sortConsultants = [...consultants];
  const userAppt = [];
  let found = false;

  for(let h = hour; h < hour + duration; h++){
    userAppt.push(h);
  }

  if(criteria == "price"){
    const rePrice = consultants.sort(function (a, b){
      return a.price - b.price;
    });
    for(let i = 0; i < rePrice.length; i++){
      const reservedCons = rePrice[i].name;
      const consSlot = timeSlot[reservedCons];

      if(userAppt.every(hour => consSlot.includes(hour))){
        console.log(reservedCons);
        consSlot.splice(hour, duration);
        found = true;
        break;
      }
    }
  } 
  else{
    const reRate = consultants.sort(function (a, b){
      return b.rate - a.rate;
    });
    for(let i = 0; i < reRate.length; i++){
      const reservedCons = reRate[i].name;
      const consSlot = timeSlot[reservedCons];

      if(userAppt.every(hour => consSlot.includes(hour))){
        console.log(reservedCons);
        consSlot.splice(hour, duration);
        found = true;
        break;
      }
    }
  }

if (!found) {
  console.log("No Service");
  }

}

const consultants = [
  { "name": "John", "rate": 4.5, "price": 1000 },
  { "name": "Bob", "rate": 3, "price": 1200 },
  { "name": "Jenny", "rate": 3.8, "price": 800 }
];

book(consultants, 15, 1, "price"); // Jenny
book(consultants, 11, 2, "price"); // Jenny
book(consultants, 10, 2, "price"); // John
book(consultants, 20, 2, "rate"); // John
book(consultants, 11, 1, "rate"); // Bob
book(consultants, 11, 2, "rate"); // No Service
book(consultants, 14, 3, "price"); // John


//Task 3
function func(...data){
  
  const midNameArr = [];
  for(i = 0; i < data.length; i++){
    if(data[i].length <= 3){
      midName = data[i].charAt(1);
    } 
    else{
      midName = data[i].charAt(2);
    }
      midNameArr.push(midName);
    }
    
  const unique = midNameArr.filter(function(char){
    return midNameArr.indexOf(char) == midNameArr.lastIndexOf(char);
  })
  const nameIndex = midNameArr.indexOf(unique[0]);
    if(unique.length == 0){
      console.log("沒有")
    }
    else{
      console.log(data[nameIndex]);    
    }

}
  
func("彭大牆","陳王明雅","吳明"); // print 彭大牆
func("郭靜雅","王立強","郭林靜宜","郭立恆","林花花"); // print 林花花
func("郭宣雅","林靜宜","郭宣恆","林靜花"); // print 沒有
func("郭宣雅","夏曼藍波安","郭宣恆"); // print 夏曼藍波安


//Task 4
function getNumber(index){
  
  let Result = 0;

  for (let num = 1; num <= index; num++){
    if (num % 3 !== 0){
      Result = Result + 4;
    }
    else{
      Result = Result - 1;
    }
  }
  return console.log(Result);
  
}

getNumber(1); // print 4
getNumber(5); // print 15
getNumber(10); // print 25
getNumber(30); // print 70
