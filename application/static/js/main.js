(function () {

    angular.module('poker', [])
    
    .config(['$interpolateProvider', function($interpolateProvider) {
        $interpolateProvider.startSymbol('{[');
        $interpolateProvider.endSymbol(']}');
    }])


    .controller('PokerController', function($scope, $compile) {
        console.log("In poker controller");
        $scope.vals = [
            'A',
            'K',
            'Q',
            'J',
            '10',
            '9',
            '8',
            '7',
            '6',
            '5',
            '4',
            '3',
            '2'
        ];
        $scope.suits = [
            '\u2660',
            '\u2665',
            '\u2666',
            '\u2663'
        ];
        $scope.cards = {
            'board1' : '',
            'board2' : '',
            'board3' : '',
            'board4' : '',
            'board5' : '',
            '11' : '',
            '12' : '',
            '21' : '',
            '22' : '',
            '31' : '',
            '32' : '',
            '41' : '',
            '42' : '',
            '51' : '',
            '52' : '',
            '61' : '',
            '62' : '',
            '71' : '',
            '72' : '',
            '81' : '',
            '82' : '',
            '91' : '',
            '92' : '',
            '01' : '',
            '02' : '',
        };
        $scope.money = {
            '1' : null,
            '2' : null,
            '3' : null,
            '4' : null,
            '5' : null,
            '6' : null,
            '7' : null,
            '8' : null,
            '9' : null,
            '0' : null,
        }
        $scope.bets = {
            '1' : null,
            '2' : null,
            '3' : null,
            '4' : null,
            '5' : null,
            '6' : null,
            '7' : null,
            '8' : null,
            '9' : null,
            '0' : null,
        }
        $scope.pot = 0;
        $scope.button = 0
        $scope.turn = 0
        
        
        $scope.send_action = function(action, bet, player) {
            console.log('Action function: ' + action + " " + bet + " " + player);
            var breaker = false;
            var turn = 1;
            while (true) {
                var template_returned = false;
                $.ajax({
                    type: 'POST',
                    // timeout: 60000,
                    url: '/action',
                    data: {
                        action: action,
                        bet: bet,
                        player: player
                    },
                }).done(function(data, textStatus, jqXHR, aaa) {
                    console.log('Received Update');
                    $scope.process_response(data);
                    if ($scope['turn'] === turn) {
                            breaker=true;
                    }
                    template_returned = true;
                });
                if (!template_returned || breaker) {
                    break;
                }
            }
        }
        
        $scope.process_response = function(game_state) {
            game_state = JSON.parse(game_state);
            console.log(game_state);
            
            $scope.$apply(function() {
                // Set up players
                var players = game_state['players'];
                for (var i=0; i < players.length; i++) {
                    var id = players[i][0]
                    $scope.money[id] = players[i][1]
                    $scope.cards[id+"1"] = 'static/imgs/' + players[i][2].toUpperCase() + ".png"
                    $scope.cards[id+"2"] = 'static/imgs/' + players[i][3].toUpperCase() + ".png"
                }
                
                var current_bets = game_state['current_bets'];
                for (var i=0; i < current_bets.length; i++) {
                    $scope.bets[i] = current_bets[i];
                }
                
                var board = game_state['board'];
                for (var i=0; i < board.length; i++) {
                    $scope.cards['board'+i] = board[i];
                }
                
                $scope.pot = game_state['pot'];
                $scope.pot = game_state['button'];
                $scope.pot = game_state['turn'];
            });
            console.log($scope.cards);
        }
    })

        
    
}());