(function(){
	var app = angular.module('store', [ ]);
	
	app.controller('StoreController', function(){
 		this.product = gem;		
	});

	var gem = {
	
		name: 'Daniel Will George',
 		price: 'Age: 27',
 		description: 'Left Brain: Computer Science, Right Brain: Actor',
	}
})();
