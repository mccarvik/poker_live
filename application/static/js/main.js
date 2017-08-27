(function () {

    angular.module('poker', [])


    .controller('PokerController', function($scope, $compile) {
        console.log("In poker controller");
        
        $scope.send_action = function(action, bet, player) {
            console.log('Action function: ' + action + " " + bet + " " + player);
            var breaker = false;
            var turn = 1;
            while (true) {
                var template_returned = false;
                $.ajax({
                    type: 'GET',
                    url: '/action',
                    data: {
                        action: action,
                        bet: bet,
                        player: player
                    },
                }).done(function(data) {
                    console.log('Finished');
                    if (data['turn'] === turn) {
                            breaker=true;
                    }
                    template_returned = true;
                });
                if (!template_returned || breaker) {
                    break;
                }
            }
        }

        $scope.getResults = function() {
          
        };
      }
    
    );
    
}());