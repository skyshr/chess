// import { isValidCastling } from './castling';

const x = ['1', '2', '3', '4', '5', '6', '7', '8'];
const y = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'];
let notations = [];

const wareCoords = {
    'Pawn': [...y.map(coordY => coordY + x[1]), ...y.map(coordY => coordY + x[6])],
    'Knight': ['B1', 'G1', 'B8', 'G8'],
    'Bishop': ['C1', 'F1', 'C8', 'F8'],
    'King': ['E1', 'E8'],
    'Queen': ['D1', 'D8'],
    'Rook': ['A1', 'H1', 'A8', 'H8'],
}

const updatePending = (board) => {
    if (notations.length) {
        let [ware, bX, bY, cX, cY] = notations[notations.length - 1];
        if (ware == 'pawn') {
            board.coords[cX][cY].ware.pending = false;
        }
    }
}

class Pawn {
    constructor(cX, cY, dir) {
        this.cX = x.indexOf(cX);
        this.cY = y.indexOf(cY);
        this.dir = dir;
        this.bool = false;
        this.pending = false;
        this.cover = [];
    }

    move(yTo, xTo, board) {
        let beforeMoveX = this.cX;
        let beforeMoveY = this.cY;
        xTo = x.indexOf(xTo);
        yTo = y.indexOf(yTo);
        if (checkValidMove(board, this, xTo, yTo)) {
            if (Math.abs(xTo - this.cX) === 2) {
                if (!this.bool) {
                    this.pending = true;
                }
                else {
                    throw new Error('Pawns can move 2 squares only if it is untouched.')
                }
            }
            this.cX = xTo;
            this.cY = yTo;
            this.bool = true;

            updatePending(board);
            notations.push(['pawn', beforeMoveX, beforeMoveY, this.cX, this.cY, this.dir]);
            
            board.updateBoard(beforeMoveX, beforeMoveY, this.cX, this.cY);
            // board.coords.forEach(xArr => {
            //     xArr.forEach(y => {
            //         if (y.ware !== '') {
            //             y.ware.updateCoveringSqrs(board);
            //         }
            //     })
            // })
        }
    }

    updateCoveringSqrs(board) {
        let [xTo, yTo] = [this.cX, this.cY];
        this.cover = [];
        let coverX, coverY;
        if (xTo > 0 && xTo < 7) {
            coverX = xTo + this.dir;
            coverY = [yTo + 1, yTo - 1].filter(y => y >= 0 && y <= 7);
            for (let y of coverY) {
                this.cover.push([coverX, y]);
            }
        }
        console.log(`Pawn pos: [${xTo}, ${yTo}], cover: `, this.cover);
    }
}

class King {
    constructor(cX, cY, dir) {
        this.cX = x.indexOf(cX);
        this.cY = y.indexOf(cY);
        this.dir = dir;
        this.bool = false;
        this.cover = [];
    }

    move(yTo, xTo, board) {
        let beforeMoveX = this.cX;
        let beforeMoveY = this.cY;
        xTo = x.indexOf(xTo);
        yTo = y.indexOf(yTo);
        if (checkValidMove(board, this, xTo, yTo)) {
            this.cX = xTo;
            this.cY = yTo;
            this.bool = true;
            
            updatePending(board);
            notations.push(['king', beforeMoveX, beforeMoveY, this.cX, this.cY, this.dir]);

            board.updateBoard(beforeMoveX, beforeMoveY, this.cX, this.cY);
            // board.coords.forEach(xArr => {
            //     xArr.forEach(y => {
            //         if (y.ware !== '') {
            //             y.ware.updateCoveringSqrs(board);
            //         }
            //     })
            // })
        }
    }

    updateCoveringSqrs(board) {
        let [xTo, yTo] = [this.cX, this.cY];
        this.cover = [];
        let xCover = [-1, 0, 1];
        let yCover = [-1, 0, 1];

        for (let x of xCover) {
            for (let y of yCover) {
                if (xTo + x >= 0 && xTo + x < 8 && yTo + y >= 0 && yTo + y < 8) {
                    if (x !== 0 || y !== 0) this.cover.push([xTo + x, yTo + y]);
                }
            }
        }

        console.log(`King pos: [${xTo}, ${yTo}], cover: `, this.cover);
    }
}

class Rook {
    constructor(cX, cY, dir) {
        this.cX = x.indexOf(cX);
        this.cY = y.indexOf(cY);
        this.dir = dir;
        this.bool = false;
        this.cover = [];
    }

    move(yTo, xTo, board) {
        let beforeMoveX = this.cX;
        let beforeMoveY = this.cY;
        xTo = x.indexOf(xTo);
        yTo = y.indexOf(yTo);
        if (checkValidMove(board, this, xTo, yTo)) {
            this.cX = xTo;
            this.cY = yTo;
            this.bool = true;
            
            updatePending(board);
            notations.push(['rook', beforeMoveX, beforeMoveY, this.cX, this.cY, this.dir]);
            
            board.updateBoard(beforeMoveX, beforeMoveY, this.cX, this.cY);
            // board.coords.forEach(xArr => {
            //     xArr.forEach(y => {
            //         if (y.ware !== '') {
            //             y.ware.updateCoveringSqrs(board);
            //         }
            //     })
            // })
        }
    }

    updateCoveringSqrs(board) {
        let [xTo, yTo] = [this.cX, this.cY];
        this.cover = [];

        for (let x = xTo - 1; x >= 0; x--) {
            this.cover.push([x, yTo])
            if (board.coords[x][yTo].ware !== '') break;
        }
        
        for (let x = xTo + 1; x < 8; x++) {
            this.cover.push([x, yTo])
            if (board.coords[x][yTo].ware !== '') break;
        }

        for (let y = yTo - 1; y >= 0; y--) {
            this.cover.push([xTo, y])
            if (board.coords[xTo][y].ware !== '') break;
        }

        for (let y = yTo + 1; y < 8; y++) {
            this.cover.push([xTo, y])
            if (board.coords[xTo][y].ware !== '') break;
        }

        console.log(`Rook pos: [${xTo}, ${yTo}], cover: `, this.cover);
    }
}

class Bishop {
    constructor(cX, cY, dir) {
        this.cX = x.indexOf(cX);
        this.cY = y.indexOf(cY);
        this.dir = dir;
        this.bool = false;
        this.cover = [];
    }

    move(yTo, xTo, board) {
        let beforeMoveX = this.cX;
        let beforeMoveY = this.cY;
        xTo = x.indexOf(xTo);
        yTo = y.indexOf(yTo);
        if (checkValidMove(board, this, xTo, yTo)) {
            this.cX = xTo;
            this.cY = yTo;
            this.bool = true;
            
            updatePending(board);
            notations.push(['bishop', beforeMoveX, beforeMoveY, this.cX, this.cY, this.dir]);
            this.updateCoveringSqrs(board, xTo, yTo);

            board.updateBoard(beforeMoveX, beforeMoveY, this.cX, this.cY);
            // board.coords.forEach(xArr => {
            //     xArr.forEach(y => {
            //         if (y.ware !== '') {
            //             y.ware.updateCoveringSqrs(board);
            //         }
            //     })
            // })
        }
    }

    updateCoveringSqrs(board) {
        let [xTo, yTo] = [this.cX, this.cY];
        this.cover = [];

        for (let k = 1; xTo - k >= 0 && yTo - k >= 0; k++) {
            this.cover.push([xTo - k, yTo - k])
            if (board.coords[xTo - k][yTo - k].ware !== '') break;
        }
        
        for (let k = 1; xTo + k < 8 && yTo - k >= 0; k++) {
            this.cover.push([xTo + k, yTo - k])
            if (board.coords[xTo + k][yTo - k].ware !== '') break;
        }

        for (let k = 1; xTo + k < 8 && yTo + k < 8; k++) {
            this.cover.push([xTo + k, yTo + k])
            if (board.coords[xTo + k][yTo + k].ware !== '') break;
        }

        for (let k = 1; xTo - k >= 0 && yTo + k < 8; k++) {
            this.cover.push([xTo - k, yTo + k])
            if (board.coords[xTo - k][yTo + k].ware !== '') break;
        }

        console.log(`Bishop pos: [${xTo}, ${yTo}], cover: `, this.cover);
    }
}

class Queen {
    constructor(cX, cY, dir) {
        this.cX = x.indexOf(cX);
        this.cY = y.indexOf(cY);
        this.dir = dir;
        this.bool = false;
        this.cover = [];
    }

    move(yTo, xTo, board) {
        let beforeMoveX = this.cX;
        let beforeMoveY = this.cY;
        xTo = x.indexOf(xTo);
        yTo = y.indexOf(yTo);
        if (checkValidMove(board, this, xTo, yTo)) {
            this.cX = xTo;
            this.cY = yTo;
            this.bool = true;
            
            updatePending(board);
            notations.push(['queen', beforeMoveX, beforeMoveY, this.cX, this.cY, this.dir]);

            board.updateBoard(beforeMoveX, beforeMoveY, this.cX, this.cY);
            // board.coords.forEach(xArr => {
            //     xArr.forEach(y => {
            //         if (y.ware !== '') {
            //             y.ware.updateCoveringSqrs(board);
            //         }
            //     })
            // })
        }
    }

    updateCoveringSqrs(board) {
        let [xTo, yTo] = [this.cX, this.cY];
        this.cover = [];

        //Bishop
        for (let k = 1; xTo - k >= 0 && yTo - k >= 0; k++) {
            this.cover.push([xTo - k, yTo - k])
            if (board.coords[xTo - k][yTo - k].ware !== '') break;
        }
        
        for (let k = 1; xTo + k < 8 && yTo - k >= 0; k++) {
            this.cover.push([xTo + k, yTo - k])
            if (board.coords[xTo + k][yTo - k].ware !== '') break;
        }

        for (let k = 1; xTo + k < 8 && yTo + k < 8; k++) {
            this.cover.push([xTo + k, yTo + k])
            if (board.coords[xTo + k][yTo + k].ware !== '') break;
        }

        for (let k = 1; xTo - k >= 0 && yTo + k < 8; k++) {
            this.cover.push([xTo - k, yTo + k])
            if (board.coords[xTo - k][yTo + k].ware !== '') break;
        }
        
        //Rook
        for (let x = xTo - 1; x >= 0; x--) {
            this.cover.push([x, yTo])
            if (board.coords[x][yTo].ware !== '') break;
        }
        
        for (let x = xTo + 1; x < 8; x++) {
            this.cover.push([x, yTo])
            if (board.coords[x][yTo].ware !== '') break;
        }

        for (let y = yTo - 1; y >= 0; y--) {
            this.cover.push([xTo, y])
            if (board.coords[xTo][y].ware !== '') break;
        }

        for (let y = yTo + 1; y < 8; y++) {
            this.cover.push([xTo, y])
            if (board.coords[xTo][y].ware !== '') break;
        }

        console.log(`Queen pos: [${xTo}, ${yTo}], cover: `, this.cover);
    }
}

class Knight {
    constructor(cX, cY, dir) {
        this.cX = x.indexOf(cX);
        this.cY = y.indexOf(cY);
        this.dir = dir;
        this.bool = false;
        this.cover = [];
    }

    move(yTo, xTo, board) {
        let beforeMoveX = this.cX;
        let beforeMoveY = this.cY;
        xTo = x.indexOf(xTo);
        yTo = y.indexOf(yTo);
        if (checkValidMove(board, this, xTo, yTo)) {
            this.cX = xTo;
            this.cY = yTo;
            this.bool = true;
            
            updatePending(board);
            notations.push(['knight', beforeMoveX, beforeMoveY, this.cX, this.cY, this.dir]);
            // this.updateCoveringSqrs(xTo, yTo);

            board.updateBoard(beforeMoveX, beforeMoveY, this.cX, this.cY);
        }
    }

    updateCoveringSqrs(board) {
        const [xTo, yTo] = [this.cX, this.cY];
        this.cover = [];

        let amountA = [2, -2];
        let amountB = [1, -1];

        let partA = amountA.map(A => amountB.map(B => [A, B])).flat();
        let partB = amountB.map(B => amountA.map(A => [B, A])).flat();
        let parts = [...partA, ...partB];
        // console.log('parts: ', parts);

        for (const [x, y] of parts) {
            // console.log('part: ', part);
            // const [x, y] = part;
            // console.log(x, y)
            if (xTo + x >= 0 && xTo + x < 8 && yTo + y >= 0 && yTo + y < 8) {
                this.cover.push([xTo + x, yTo + y]);
            }
        }

        console.log(`Knight pos: [${xTo}, ${yTo}], cover: `, this.cover);
    }

}

const isValidPawnMove = (board, x, y, dir, xTo, yTo) => {
    let obs1 = board.coords[x + dir][yTo];
    let obs2 = board.coords[x + 2 * dir][yTo];

    if (x + dir === xTo) {
        if (y === yTo) {
            if (obs1.ware === '') {
                return true;
            }
            else throw new Error(`Pawns can only take opponent's wares diagonally!`);
        }
        else if (y + dir === yTo || y - dir === yTo) {
            if (obs1.ware === '') {
                let isEnpassantWare = board.coords[x][yTo];
                if (dir !== isEnpassantWare.dir && isEnpassantWare instanceof Pawn && isEnpassantWare.pending) {
                    return true;
                }
                else {
                    throw new Error(`Pawns can't move diagonally if there is no ware in a square!`);
                }
            }
            else if (obs1.dir === dir) {
                throw new Error(`Pawns can only take opponent's wares diagonally!`);
            }
            else if (obs1 instanceof King) {
                throw new Error(`Cannot take opponent's king!`);
            }
            return true;
        } 
        else throw new Error('Invalid Pawn Move!');
    }
    else if (x + 2 * dir == xTo) {
        if (y == yTo) {
            if (obs1.ware !== '' || obs2.ware !== '' ) {
                throw new Error(`There exists a piece in the pawn's way!`);
            }
            return true;
        }
        else throw new Error('Invalid Pawn Move!');
    }
    else throw new Error('Invalid Pawn Move!');
}

const isValidKingMove = (board, dir, xTo, yTo) => {
    let obs = board.coords[xTo][yTo].ware;
    // check if allocated piece is defended 
    if (obs !== '' && dir === obs.dir) {
        throw new Error("Kings can only move to squares that are empty or that has an oppeonent's piece that is undefended.");
    }
    return true;
}

const isValidRookMove = (board, x, y, dir, xTo, yTo) => {
    if (x === xTo) {
        for (let j = y + 1; j < yTo; j++) {
            if (board.coords[x][j].ware !== '') {
                throw new Error("There exists a piece in the rook's way!");
            }
        }
    }
    else {
        for (let i = x + 1; i < xTo; i++) {
            if (board.coords[i][y].ware !== '') {
                throw new Error("There exists a piece in the rook(queen)'s way!");
            }
        }
    }
    if (board.coords[xTo][yTo].ware === '') return true;
    if (dir === board.coords[xTo][yTo].ware.dir) {
        throw new Error("Cannot take allies' piece!");
    }
    else if (board.coords[xTo][yTo].ware instanceof King) {
        throw new Error(`Cannot take opponent's king!`);
    }
    return true;
}

const isValidBishopMove = (board, x, y, dir, xTo, yTo) => {
    let signX = x < xTo ? 1 : -1;
    let signY = y < yTo ? 1 : -1;
    let checkBool = true;

    while (x + signX !== xTo) {
        if (board.coords[x + signX][y + signY].ware !== '') {
            checkBool = false;
            break;
        }
        signX += signX / Math.abs(signX);
        signY += signY / Math.abs(signY);
    }

    if (!checkBool) {
        throw new Error("There exists a piece in the bishop(queen)'s way!");
    }
    else {
        if (board.coords[xTo][yTo].ware === '') return true;
        if (dir === board.coords[xTo][yTo].ware.dir) {
            throw new Error("Cannot take allies' piece!");
        }
        else if (board.coords[xTo][yTo].ware instanceof King) {
            throw new Error(`Cannot take opponent's king!`);
        }
        return true;
    }
}

const isValidKnightMove = (board, x, y, dir, xTo, yTo) => {
    let obs = board.coords[xTo][yTo].ware;
    if (obs === '') return true;
    if (dir === obs.dir) {
        throw new Error("Cannot take allies' piece!");
    }
    if (obs instanceof King) {
        throw new Error(`Cannot take opponent's king!`);
    }
    return true;
}

const checkValidMove = (board, ware, xTo, yTo) => {
    let [x, y, dir, bool] = [ware.cX, ware.cY, ware.dir, ware.bool];
    if (dir === board.dir) {
        if (xTo >= 0 && xTo <= 7 && yTo >= 0 && yTo <= 7) {
            if (x == xTo && y == yTo) {
                return false;
            }
    
            if (ware instanceof Pawn) {
                return isValidPawnMove(board, x, y, dir, xTo, yTo);
            }
    
            else if (ware instanceof King) {
                // if (x === xTo && Math.abs(y - yTo) === 2) {
                //     if (!bool) {
                //         let [checkX, checkY] = y > yTo ? [x, 0] : [x, 7];
                //         let checkBool = board.coord[checkX][checkY].ware.bool;
                //         if (!checkBool) {
                //             let squareArr = checkY > y ? [5, 6] : [1, 2, 3]
                //             if (checkY)
                //             return isValidCastling(board, x, squareArr)
                //         }
                //         throw new Error('Rook has moved hence not allowed to castle!');
                //     }
                //     else {
                //         throw new Error('King has moved hence not allowed to castle!');
                //     }
                // }
                // else 
                if (Math.abs(x - xTo) >= 2 || Math.abs(y - yTo) >= 2) {
                    throw new Error('King move out of bounds...');
                }
                return isValidKingMove(board, dir, xTo, yTo);
            }
    
            else if (ware instanceof Rook) {
                if (x !== xTo && y !== yTo) throw new Error('Invalid Rook Move!');
                return isValidRookMove(board, x, y, dir, xTo, yTo);
            }
    
            else if (ware instanceof Bishop) {
                if (Math.abs(xTo - x) !== Math.abs(yTo - y)) throw new Error('Invalid bishop move!');
                return isValidBishopMove(board, x, y, dir, xTo, yTo);
            }
    
            else if (ware instanceof Queen) {
                if (x !== xTo && y !== yTo && Math.abs(xTo - x) !== Math.abs(yTo - y)) {
                    throw new Error('Invalid queen move!');
                }
                if (x === xTo || y === yTo) return isValidRookMove(board, x, y, dir, xTo, yTo);
                return isValidBishopMove(board, x, y, dir, xTo, yTo);
            }
    
            else if (ware instanceof Knight) {
                let difX = Math.abs(x - xTo);
                let difY = Math.abs(y - yTo);
                if ((difX === 1 && difY === 2) || (difX === 2 && difY === 1)) {
                    return isValidKnightMove(board, x, y, dir, xTo, yTo);
                }
                else throw new Error('Invalid knight move!');
            }
    
            return false;
        }
        else throw new Error('Invalid Move!');
    }
    else throw new Error(`It is opponent's turn.`);
}

const findWare = (cY, cX) => {
    let ware = Object.keys(wareCoords).find(ware => wareCoords[ware].includes(cY + cX));
    return ware === undefined ? '' : placeWare(ware, cX, cY);
}

const placeWare = (ware, cX, cY) => {
    let dir = parseInt(cX) <= 2 ? 1 : -1;
    if (ware === 'Pawn') {
        return new Pawn(cX, cY, dir);
    }
    else if (ware === 'King') {
        return new King(cX, cY, dir);
    }
    else if (ware === 'Rook') {
        return new Rook(cX, cY, dir);
    }
    else if (ware === 'Bishop') {
        return new Bishop(cX, cY, dir);
    }
    else if (ware === 'Queen') {
        return new Queen(cX, cY, dir);
    }
    else if (ware === 'Knight') {
        return new Knight(cX, cY, dir);
    }
    return ware;
}

class Board {
    constructor() {
        this.coords = x.map((coordX) => y.map(coordY => new Coordinate(coordY, coordX)))
        this.dir = 1;
        this.updateDetails();
    }

    updateBoard(beforeX, beforeY, afterX, afterY) {
        let cWare = this.coords[beforeX][beforeY].ware;
        this.coords[beforeX][beforeY].updateCoords();
        this.coords[afterX][afterY].updateCoords(cWare);
        this.dir *= -1;
        
        this.updateDetails();
    }

    updateDetails() {
        this.coords.forEach(xArr => {
            xArr.forEach(y => {
                if (y.ware !== '') {
                    y.ware.updateCoveringSqrs(this);
                }
            })
        })
    }
    //     defendedWhite = [];
    //     defendedBlack = [];
    //     attackWhite = [];
    //     attackBlack = [];

    //     for (let x = 0; x < 8; x++) {
    //         for (let y = 0; y < 8; y++) {
    //             let ware = this.coords[x][y].ware;
    //             let dir = ware.dir;
    //             if (ware instanceof Pawn) {

    //             } 
    //         }
    //     }
    // }

    printCoords() {
        console.log(this.coords);
    }
}

class Coordinate {
    constructor(y, x, ware = findWare(y, x)) {
        this.x = x;
        this.y = y;
        this.ware = ware;
    }

    updateCoords(ware = '') {
        this.ware = ware;
    }

    printInfos() {
        console.log(this.x, this.y, this.ware);
    }
}

let A = new Board();
// A.printCoords();
// console.log(A.coords);
// console.log(A.coords[1][0].ware);
// A.coords[1][0].ware.move(3, 0, A);
// console.log(A.coords);

// A.coords[6][0].ware.move(4, 0, A);
// A.coords[1][1].ware.move(3, 1, A);
// A.coords[4][0].ware.move(3, 1, A);
// A.coords[3][0].ware.move(4, 0, A);
// console.log(A.coords);
// console.log(A.coords[3][0].ware);
// console.log(A.coords[3][1].ware);

//King
// A.coords[1][4].ware.move('E', '4', A);

// A.coords[1][4].ware.move(3, 4, A);
// A.coords[6][4].ware.move(4, 4, A);
// A.coords[3][4].ware.move(5, 4, A);
// console.log(A.coords[3][4].ware);
// A.coords[0][4].ware.move(1, 4, A);
// console.log(A.coords);
// console.log(A.coords[3][4].ware);
// console.log(A.coords[1][4].ware);
// A.coords[0][4].ware.move(2, 2, A);
// A.coords[3][0].ware.move(4, -1, A);
// A.coords[3][0].ware.move(4, 1, A);
// console.log(A.coords);

//Rook
// A.coords[1][0].ware.move(3, 0, A);
// console.log(A.coords[3][0].ware);
// A.coords[3][0].ware.move(4, 0, A);
// console.log(A.coords[4][0].ware);
// A.coords[0][0].ware.move(0, 5, A);
// A.coords[0][0].ware.move(3, 0, A);
// console.log(A.coords[3][0].ware);
// A.coords[0][0].ware.move(4, 0, A);
// A.coords[0][0].ware.move(5, 0, A);
// A.coords[0][4].ware.move(2, 2, A);

//Bishop
// A.coords[0][2].ware.move(1, 2, A);
// A.coords[0][2].ware.move(1, 3, A);
// A.coords[0][2].ware.move(2, 0, A);
// A.coords[1][1].ware.move(3, 1, A);
// A.coords[0][2].ware.move(1, 1, A);
// A.coords[1][1].ware.move(4, 4, A);
// A.coords[4][4].ware.move(6, 6, A);
// console.log(A.coords[6][6].ware);
// console.log(A.coords);

//Queen
// A.coords[0][3].ware.move(1, 2, A);
// A.coords[0][3].ware.move(1, 5, A);
// A.coords[0][3].ware.move(2, 5, A);
// A.coords[1][2].ware.move(3, 2, A);
// A.coords[0][3].ware.move(3, 0, A);
// A.coords[3][0].ware.move(7, 0, A);
// A.coords[3][0].ware.move(6, 0, A);
// A.coords[3][0].ware.move(6, 3, A);
// A.coords[6][3].ware.move(7, 4, A);
// console.log(A.coords)


const checkWare = (coordX, coordY, myDir, opDir) => {
    if (myDir * opDir !== -1) return -1;
    return findWare(coordX, coordY);
}

// let p = new Pawn(0, 0, 1);
// console.log(p.x, p.y);
// p.move(4);
// console.log(p.x, p.y);
// p.move(4);
// console.log(p.x, p.y);
// p.move(1);
// console.log(p.x, p.y);



// let B = new Coordinate('A', '1');
// B.printInfos();

// let C = new Coordinate('B', '2', 'Pawn');
// C.printInfos();

// let D = new Coordinate('E', '1');
// D.printInfos();