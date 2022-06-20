$(document).on('submit', '#game-board-form', function(e) {
    e.preventDefault();

    // Play the move locally before the AI starts to think
    const clickedCell = $(document.activeElement);
    const cellId = clickedCell.attr('id');
    if (clickedCell.hasClass('playerCell') || clickedCell.hasClass('aiCell')) {
        return;
    }
    
    // Get values of game settings set by the user
    const boardSize = $('#board_size').val()
    const mctsIterations = $('#mcts_iterations').val()
    if (mctsIterations > 100000 || mctsIterations < 1) {
        alert('MCTS iterations too high. Try a value between 1 and 100,000');
        return;
    }
    
    // Let the AI think, then update the UI with the AI's move
    if (clickedCell.attr('name') !== 'reset') {
        clickedCell.addClass('playerCell');
        clickedCell.text('O');
        $("#game-state-info h4").text("AI is thinking...");
        $('.cell').attr("disabled", true);
    }

    $.ajax({
        type: 'POST',
        url: '/play',
        data: {
            cell: cellId,
            board_size: boardSize,
            mcts_iterations: mctsIterations
        },
        success: function(response) {
            const { board, game_state_message } = response;
            $('.cell').attr("disabled", false);
            let cellPos = 1;
            if (game_state_message) {
                $("#game-state-info h4").text(game_state_message);
            } else {
                $("#game-state-info h4").text("Player's Turn");
            }
            for (let i = 0; i < board.length; i++) { 
                for (let j = 0; j < board[0].length; j++) {
                    const player = board[i][j];
                    let cellOnBoard = $(`#game-board-form button[id='${cellPos}']`);
                    switch (player) {
                        case 1:
                            cellOnBoard.text('O');
                            cellOnBoard.removeClass('blankCell');
                            cellOnBoard.addClass('playerCell');
                            break;
                        case -1:
                            cellOnBoard.text('X');
                            cellOnBoard.removeClass('blankCell');
                            cellOnBoard.addClass('aiCell');
                            break;
                        default:   
                            cellOnBoard.text('');
                            cellOnBoard.removeClass('playerCell');
                            cellOnBoard.removeClass('aiCell');
                            cellOnBoard.addClass('blankCell');
                            cellOnBoard.prop("disabled", false);
                            break;
                    }
                    if (game_state_message !== null) {
                        cellOnBoard.prop("disabled", true);
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

// Game controls radio button
$("#board_size").on("change", function(e) {
    const boardSize = $(this).val();
    $.ajax({
        type: 'POST',
        url: '/board',
        data: {
            board_size: boardSize
        },
        success: function(response) {
            $("#game-board-form").replaceWith(response);
            $("#game-board").css( "grid-template", `repeat(${boardSize}, 1fr) / repeat(${boardSize}, 1fr)`);
            // Adjust the font size of the cells
            const newFontSize = 48 - ((boardSize - 3) * 10);
            $(".cell").css("font-size", newFontSize);
        },
        error: function() {
            alert('error');
        }
    })
});