const isValidCastling = (board, x, squareArr) => {
    // 1. Check if there are any pieces between king allies' castling-side rook.
    if (isCastlingSquaresEmpty(board, x, squareArr)) {
    // 2. Check if the castling-covering-squares are safe from opponent's attack.
        return isCastlingSquaresSafe(board, x, squareArr)
    }
}

const isCastlingSquaresEmpty = (board, x, squareArr) => {
    for (let y of squareArr) {
        if (board.coords[x][y].ware !== "") {
            throw new Error('Failed Castling - there exists a piece in the way!')
        }
    }
    return true;
}

const isCastlingSquaresSafe = (board, x, squareArr) => {
    for (let y of squareArr) {
        if (board.coords[x][y])
    }
}

export default {isValidCastling};
