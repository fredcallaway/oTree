/* jshint esversion: 6 */
// THIS IS THE WRONG FILE IT SEEMS!!!! Looking parent folde _static/global/interface.js

function render_game(game) {
  let result = ["<table class='game-table' border=2>"];
  game.forEach((row, i) => {
    result.push(`<tr class='game-row' value='${i}'>`);
    // result.push('<td><button class="btn btn-secondary">X</button></td>');
    row.forEach((cell, j) => {
      result.push(`<td class='game-cell game-row-${i} game-col-${j} '>&nbsp;
        <payouts><rowpay>${cell[0]}</rowpay>  |  <colpay>${cell[1]}</colpay></payouts>
        &nbsp;</td>`
      );
    });
    result.push("</tr>");
  });
  result.push("</table>");
  return result.join('\n');
}

function showResult(target, game, row, col) {
  console.log('showResult', row, col);
  $(target).append(render_game(game));
  $('.game-row').removeClass('game-row');

  $(`.game-row-${row}`)
    .addClass('chosen')
    .removeClass('unchosen');

  $('.game-cell').addClass('unchosen');
  $(`.game-col-${col}`).addClass('chosen');
  $(`.game-col-${col}.game-row-${row}`)
    .addClass('chosen')
    .removeClass('unchosen')
  ;
}

function runGame(target, game) {

  let msg = $('<div>', {id: 'game-msg'});
  let rowmsg = $('<div>').appendTo(msg);
  let colmsg = $('<div>').appendTo(msg);
  $('.otree-btn-next').prop('disabled', true);

  $(target)
    .append(render_game(game))
    .append(msg)
  ;

  rowmsg.html('Please choose a row.');

  $('.game-row').click(function() {
    let row = parseInt($(this).attr('value'));

    rowmsg.html(`You chose row ${row+1}.`);

    $('.game-cell').addClass('unchosen');
    for (let i in game) {
      if (i == row) {
      // Mark chosen row
        $(`.game-row-${i}`)
          .removeClass('unchosen')
          .addClass('chosen')
        ;
      }
      else {
        $(`.game-row-${i}`)
          .removeClass('chosen')
          .addClass('unchosen')
        ;
      }
    }

    $('#id_choice').val(String(row));  // record choice
    $('.otree-btn-next').prop('disabled', false);
  });
}
