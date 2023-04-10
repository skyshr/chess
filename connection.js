let arr = [
    ['.', '.', 'A', 'A', 'B', '.', '.', 'C'],
    ['E', 'D', 'D', 'D', 'A', 'B', '.', 'C'],
    ['A', '.', '.', 'A', '.', '.', 'B', 'B'],
    ['A', 'A', 'A', '.', '.', 'C', 'B', 'C'],
    ['.', '.', '.', 'D', 'D', '.', '.', 'C'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['F', 'F', 'F', 'F', 'F', 'F', 'F', 'F'],
    ['F', 'A', 'B', 'C', '.', '.', 'E', 'E'],
]; 
// [['A','A','B','E','D','D','D','A','B','A','A','A','A','A'],
// ['D', 'D'], ['C', 'C', 'B', 'B', 'C' ,'B', 'C', 'C'],
// ['F','F','F','F','F','F','F','F','F','A','B','C','E','E']]

let stack = [];
let visit = {};

for (let x = 0; x < arr.length; x++) {
    for (let y = 0; y < arr.length; y++) {
        if (arr[x][y] !== '.') {
            visit[String(x)+y] = false;
            stack.push(String(x)+y)
        }
    }
}
let finalArr = [];
let res = [];

const validArr = (str) => {
    let [x, y] = [+str[0], +str[1]];
    let [min, max] = [0, 7];
    let filtered = [[x - 1, y], [x + 1, y], [x, y - 1], [x, y + 1]].filter(coord => coord[0] >= min && coord[1] <= max);
    return filtered.map(coord => String(coord[0])+coord[1]);
}

while(stack.length) {
    let str = stack.pop();
    if (!visit[str]) {
        let result = validArr(str);
        for (let coordS of result) {
            if (stack.indexOf(coordS) !== -1 && !visit[coordS]) stack.push(coordS);
        }
        visit[str] = true;
        res.push(str);
    }
    else {
        if (res.length) finalArr.push(res);
        res = [];
    }
}
console.log(finalArr);
finalArr = finalArr.map(a => a.map(b => arr[+b[0]][+b[1]]));

