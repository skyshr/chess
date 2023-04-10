// let arr = [];
// console.log(arr.reduce((a,b) => a + b, 0))

// function solution(enroll, referral, seller, amount) {
//     var answer = [];
//     let m = new Map();
//     let filtered = enroll.filter(enr => referral.indexOf(enr) == -1);
    
//     for (let i = 0; i < seller.length; i++) {
//         let p = amount[i] * 100;
//         let start = seller[i];
//         while(start !== '-') {
//             let findIdx = enroll.indexOf(start);
//             let sal = parseInt(p * 0.1);
//             p -= sal;
//             if (m.has(start)) {
//                 m.set(start, m.get(start) + p)
//             }
//             else m.set(start, p);
//             p = sal;
//             start = referral[findIdx]
//         }
//     }
    
//     // console.log('filtered:' ,filtered);

//     enroll.forEach((enr) => {
//         answer.push(m.has(enr) ? m.get(enr) : 0)
//     })
    
//     return answer;
// }

// function solution1(enroll, referral, seller, amount) {
//     var answer = [];
//     let m = new Map();
//     let filtered = enroll.filter(enr => referral.indexOf(enr) == -1);

//     for (let i = 0; i < filtered.length; i++) {
//         let start = filtered[i];
//         let price = [];
//         while(start !== '-') {
//             let findIdx = enroll.indexOf(start);
//             if (seller.indexOf(start) !== -1 && !m.has(start)) {
//                 let tmp = amount[seller.indexOf(start)] * 100;
//                 price.push(tmp);
//                 // s.push(start);
//             }
//             let total = price.reduce((a,b) => a + b, 0);
//             price = price.map(p => parseInt(p * 0.1));
//             let calTot = price.reduce((a,b) => a + b, 0);
//             // console.log(total, calTot)
            
//             if (m.has(start)) {
//                 m.set(start, m.get(start) + total - calTot);
//             }
//             else {
//                 m.set(start, total - calTot);
//             }   
//             // console.log('start : ', start);
//             // console.log('price :', price);
//             // console.log(m);
            
//             start = referral[findIdx];
//         }
//     }
    
//     enroll.forEach((enr) => {
//         answer.push(m.has(enr) ? m.get(enr) : 0)
//     })
    
//     return answer;
// }

function solution (enroll, referral, seller, amount) {
    const tree = { "minho" : [] };
    enroll.forEach(name => tree[name] = []);
    
    for(const [idx, ref] of referral.entries()) {
      const target = ref === '-' ? "minho" : ref;
      tree[target].push(enroll[idx]);
    }

    console.log('tree: ', tree);
    
    const sales = seller.reduce((acc, cur, idx) => {
      const cost = amount[idx] * 100;
      acc[cur] ? acc[cur].push(cost) : acc[cur] = [ cost ];
      return acc;
    }, {});

    console.log('sales: ', sales)
    
    const stack = [ ["minho", null] ];
    const visit = { "minho" : false };
    enroll.forEach(name => visit[name] = false);
    
    while(stack.length) {
      const [cur, parent] = stack.pop();
    //   console.log(`cur: ${cur}, parent: ${parent}`);
      
      if(visit[cur]) {
        if(sales[cur] && cur !== "minho") {
            console.log('cur: ', cur);
            console.log(sales[cur]);
          for(let i = 0; i < sales[cur].length; i++) {
            const income = sales[cur][i] < 10 ? 0 : sales[cur][i] * 0.1 >> 0;
            console.log('income: ', income)
            sales[parent] ? sales[parent].push(income) : sales[parent] = [ income ];
            sales[cur][i] -= income;
          }
        }
        continue;
      }
      
      stack.push([cur, parent]);
      visit[cur] = true;
      
      for(const next of tree[cur]) {
        if(!visit[next]) {
          stack.push([next, cur]);
        }
      }
      console.log('stack: ', stack);
    }
    
    const answer = enroll.map(name => sales[name] ? sales[name].reduce((a, b) => a+b) : 0);
    
    return answer;
  }

console.log(solution(["john", "mary", "edward", "sam", "emily", "jaimie", "tod", "young"], ["-", "-", "mary", "edward", "mary", "mary", "jaimie", "edward"], ["young", "john", "tod", "emily", "mary"], [12, 4, 2, 5, 10]));
// console.log(solution1(["john", "mary", "edward", "sam", "emily", "jaimie", "tod", "young"], ["-", "-", "mary", "edward", "mary", "mary", "jaimie", "edward"], ["young", "john", "tod", "emily", "mary"], [12, 4, 2, 5, 10]))

// console.log(solution(["john", "mary", "edward", "sam", "emily", "jaimie", "tod", "young"], ["-", "-", "mary", "edward", "mary", "mary", "jaimie", "edward"], ["young", "john", "tod", "emily", "mary", "edward", "sam", "jaimie"], [12, 4, 2, 5, 10, 444, 999, 5]))
// console.log(solution1(["john", "mary", "edward", "sam", "emily", "jaimie", "tod", "young"], ["-", "-", "mary", "edward", "mary", "mary", "jaimie", "edward"], ["young", "john", "tod", "emily", "mary", "edward", "sam", "jaimie"], [12, 4, 2, 5, 10, 444, 999, 5]))



