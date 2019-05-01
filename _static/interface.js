/* jshint esversion: 6 */

function render_game(game) {
  let result = ["<table class='game-table' border=2>"];
  game.forEach((row, i) => {
    result.push(`<tr class='game-row' value='${i}'>`);
    // result.push('<td><button class="btn btn-secondary">X</button></td>');
    row.forEach((cell, j) => {
      result.push(`<td class='game-cell game-row-${i} game-col-${j} '>&nbsp;
        <payouts><rowpay>${format_num(cell[0],1)}</rowpay>  |  <colpay>${format_num(cell[1],1)}</colpay></payouts>
        &nbsp;</td>`
      );
    });
    result.push("</tr>");
  });
  result.push("</table>");
  return result.join('\n');
}
function format_num(num, length) {
    var r = "" + num;
    while (r.length < length) {
        r = "\xa0\xa0" + r;
        // r =  r.padStart(1, "0");
    }
    return r;
}

function showResult(target, game, row, col) {
  console.log('showResult', row, col);
  $(target).append(render_game(game));
  $(`${target} .game-row`).removeClass('game-row');

  $(`${target} .game-row-${row}`)
    .addClass('chosen')
    .removeClass('unchosen');

  $(`${target} .game-cell`).addClass('unchosen');
  $(`${target} .game-col-${col}`).addClass('chosen');
  $(`${target} .game-col-${col}.game-row-${row}`)
    .addClass('chosen')
    .removeClass('unchosen')
  ;
}

function makeTimer(seconds) {
  console.log("makeTimer");
  var seconds_left = seconds;
  $("#timer_span").text(seconds_left);
  return new Promise(function(resolve) {
    var interval = setInterval(function() {
      $('#timer_span').text(--seconds_left);
      if (seconds_left == 0) {
        $("#timer_span").text("&nbsp;");
        clearInterval(interval);
        resolve();
      }
      console.log(seconds_left);
    }, 1000);
  });
}

function showGame(target, game) {
  $(target)
    .append(render_game(game))
  ;
  $('.game-row').removeClass('game-row');
}

function runGame(target, game, min_time) {
  $('#please_wait').hide();

  let msg = $('<div>', {id: 'game-msg'});
  let rowmsg = $('<div>').appendTo(msg);
  let colmsg = $('<div>').appendTo(msg);
  $('.otree-btn-next').prop('disabled', true);

  $(target)
    .append(render_game(game))
    .append(msg)
  ;

  rowmsg.html('Please choose a row.');
  var timer = makeTimer(min_time);


  $('.game-row').click(function() {
    $('#please_wait').show();
    timer.then(value => {
      $('.otree-btn-next').prop('disabled', false);
      $('#please_wait').hide();
    });
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
    // $('.otree-btn-next').prop('disabled', false);
  });
}
