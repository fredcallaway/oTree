var $ = require('jquery');
var runGame = require('./normal-form-games.js');

var game = [
  [[3, 3], [0, 6], [1, 5]],
  [[6, 0], [0, 0], [2, 6]],
  [[2, 3], [2, 8], [4, 1]],
];

$(document).ready(function () {
  runGame('#target', game);
});

