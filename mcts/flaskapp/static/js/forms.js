$(document).on('submit','#game-board-form', function(e) {
    e.preventDefault();

    // Play the move locally before the AI starts to think
    const clickedCell = $(document.activeElement);
    const cellId = clickedCell.attr('id');

    // Let the AI think
    $.ajax({
        type: 'POST',
        url: '/play',
        data: {
            cell: cellId
        },
        success: function(board) {
            // Update the UI with the AI's move
            let cellPos = 1;
            console.log('board', board);
            for (let i = 0; i < board.length; i++) { 
                for (let j = 0; j < board[0].length; j++) {
                    const player = board[i][j];
                    let cellOnBoard = $(`#game-board-form button[id='${cellPos}']`);
                    switch (player) {
                        case 1:
                            cellOnBoard.text('O');
                            break;
                        case -1:
                            cellOnBoard.text('X');
                            break;
                        default:   
                            cellOnBoard.text('');
                            break;
                    }
                    cellPos += 1;
                }
            }  
        },
        error: function() {
            alert('error');
        }
    })
});