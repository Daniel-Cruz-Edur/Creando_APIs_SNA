let Numbers = [1,2,3,4,5];

console.log(Numbers);


console.log(Numbers[0] + Numbers[4]);
console.log(Numbers[0] + Numbers[0]);

//Add an element to array
Numbers[3] = 3.5;
console.log(Numbers);

Numbers.push(6);
console.log(Numbers);


let Last = Numbers.pop();
console.log(Last);
console.log(Numbers);


let City = ['Bogota','Cali','Manizalez','Medellin','Armenia','Pereira','Ibague','Pasto'];

for(let Index=0; Index <= Numbers.length; Index++)
{
    console.log('Elemento' + Numbers[Index]);
}


/* 10 5 8 20 3 15 */

