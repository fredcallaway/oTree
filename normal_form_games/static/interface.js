/* jshint esversion: 6 */

function render_game(game) {
  let result = ["<table border=2>"];
  game.forEach((row, i) => {
    result.push(`<tr class='nfg-row' value='${i}'>`);
    // result.push('<td><button class="btn btn-secondary">X</button></td>');
    row.forEach((cell, j) => {
      result.push(`<td class='nfg-cell nfg-row-${i} nfg-col-${j} '>&nbsp;
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
  $('.nfg-row').removeClass('nfg-row');

  $(`.nfg-row-${row}`)
    .addClass('chosen')
    .removeClass('unchosen');

  $('.nfg-cell').addClass('unchosen');
  $(`.nfg-col-${col}`).addClass('chosen');
  $(`.nfg-col-${col}.nfg-row-${row}`)
    .addClass('chosen')
    .removeClass('unchosen')
  ;
  // let outcome = game[row][col];
}

function runGame(target, game) {

  let msg = $('<div>', {id: 'nfg-msg'});
  let rowmsg = $('<div>').appendTo(msg);
  let colmsg = $('<div>').appendTo(msg);

  $(target)
    .append(render_game(game))
    .append(msg)
  ;

  rowmsg.html('Please choose a row.');

  $('.nfg-row').click(function() {
    let row = parseInt($(this).attr('value'));
    console.log(row);
    rowmsg.html(`You chose row ${row+1}.`);
    colmsg.html('Waiting for the other player...');
    $('.nfg-row').removeClass('nfg-row');
    $('.nfg-cell').addClass('unchosen');
    $(`.nfg-row-${row}`)
      .addClass('chosen')
      .removeClass('unchosen');
    $('#id_choice').val(String(row));
  });
}