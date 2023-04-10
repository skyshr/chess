// S(n) = S(n-2) + S(n-3) + S(n-4) + 3 * S(n - 5) + 3 *S(n - 6) + S(n - 7) (n > 7)

function solution(k) {
    let d = {'0': 6, '1': 2, '2': 5, '3': 5, '4': 4, '5': 5, '6': 6, '7': 3, '8': 7, '9': 6};
    let arr = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'];
    let sol = [0, 0, 1, 1, 2, 5, 6, 12, 19];

    var answer = new Set();
    function DFS(S, str) {
        if (S < 0) return;
        if (S === 0) {
            answer.add(str);
            return;
        }
        else {
            for (let i = 0; i < arr.length; i++) {
                if (i === 0 && str === "") continue;
                DFS(S - d[arr[i]], str + arr[i])
            }
        }
    }
    DFS(k, '');
    if (k === 6) answer.add(6)

    // console.log(answer)

    return answer.size;
}

let sol = [0, 0, 1, 1, 2, 5, 6, 12];
function solution1(k) {
    let start = 8;
    let data;
    for (start; start <= k; start++) {
        data = sol[start-2] + sol[start-3] + sol[start - 4] + 3 * sol[start - 5] + 3 * sol[start - 6] + sol[start - 7];
        sol.push(data);
    }
    return data;
}

// console.log(solution(30));
console.log(solution1(30));

// let data = [];

// for (let i = 1; i <= 30; i++) {
//     // data.push(solution(i))
//     console.log('sol: ', solution(i));
//     console.log('sol1: ', solution1(i));
// }

// console.log(4292 + 2506 + 1463 +  3 * 854 + 3 * 496 + 290)

// console.log(data)
