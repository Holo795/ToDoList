function get_days(nb) {
  var array = []
  for (i = 1; i <= nb; i++) {
    array.push(i);}
  return array
}


var current_date = new Date();
console.log(current_date)

var year = []

for (i=1; i<=13; i++) {
  if (i % 2 === 1) {
    year.push(get_days(31))
  } 
}

console.log(year);
