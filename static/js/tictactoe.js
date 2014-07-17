(function($) {
  /**
   * Setup view prompts user for info and posts responses
   * to server
   */
  var SetupView = Backbone.View.extend({
    el: $('#modal-one'),
    modalEl: $('#modal-one > .modal-dialog'),
    
    //template fragement
    templateOrder: _.template($('#template-step2').html()),

    events: {
      "click .modal-marker-pref"   : "setMarker",
      "click .modal-game-order"    : "setOrder"
    },

    initialize: function(){
      this.mark = 'O';
      this.computer = 'X';
      this.order = '1';

      this.listenTo(bus, "setupView:closeModal", this.closeModal);
    },

    setMarker: function(e){
      e.preventDefault();

      // Save the player's selected mark
      if ($(e.target).text() == 'X'){
        this.mark = 'X';
        this.computer = 'O';
      }

      this.modalEl.html(this.templateOrder());
      //Transitions
      $('#order-q').fadeIn();
      $('.modal-game-order').fadeIn();

    },

    setOrder: function(e){
      e.preventDefault();

      if ($(e.target).text() == 'No'){
        this.order = '2';
      }

      this.initGame();
    },

    //
    // Set up game config like order (i.e., computer plays first) 
    // and marker.
    //
    initGame: function(){
      var self = this;
      var actor = 'You have';

      if (self.order != '1'){ actor = 'Computer has'; }
      
      $.post('/init', {order: self.order, mark: self.mark}, function(data){
        if(data.success){
          $('.modal-header > h1').text(actor+' first move. Good luck!');
          $('.modal-game-order').hide();
          
          if (self.order != '1') {bus.trigger('appView:computerMove');}
          bus.trigger('setupView:closeModal');
        }
      });
    },

    //
    // Automatically close start-up modal
    //
    closeModal: function(){
      setTimeout(function (){
        window.location.hash = '';
      }, 1500);
    }

  });

  /**
   * A simple View for generating table cells
   *
   */
  var CellView = Backbone.View.extend({
    
    template: _.template($('#template-cell').html()),

    events: {
      "click"   : "updateCell"
    },

    render: function(){
      this.$el.html(this.template(this.model.toJSON()));
      return this;
    },

    // Adds X or O to cell when clicked
    updateCell: function(e){
      this.model.set('open', false);
      bus.trigger('appView:postMove', this.model.get('id'));
    }
  });

  
  /**
   * TTT app entry point (i.e., controller)
   */
  var AppView = Backbone.View.extend({
    
    el: $('#tictactoe'),
    announceEl: $('#announce'),
    modalEl: $('#modal-one > .modal-dialog'),

    //template fragement
    templateMarker: _.template($('#template-step1').html()),

    initialize: function(){
      this.total_moves = 0;
      this.listenTo(bus, "appView:postMove", function(id){
        this.setMove(id);
      });
      this.listenTo(bus, "appView:computerMove", this.getComputerMove);
      this.listenTo(bus, "appView:endGame", this.refreshModal);
      this.gameInit = new SetupView;

      //lives outside of tictactoe element
      $('#restart').bind('click', this.restartGame);

      this.refreshModal();
      window.location.hash = 'modal-one';
    },

    //Transitions
    refreshModal: function(){
      this.modalEl.html(this.templateMarker());
    },

    render: function(){
      Board.each(this.addCell, this);
    },

    // Helper that adds cell to grid DOM element
    addCell: function(cell){
      var view = new CellView({model: cell});
      this.$('#grid').append(view.render().el);
    },

    // Posts the players position to the server
    setMove: function(id){
      var self = this;
      var payload = {position: id, mark: self.gameInit.mark};

      $.post('/play', payload, function(data){
        self.$el.find('.cell'+data.position).text(self.gameInit.mark);
        this.total_moves = ++this.total_moves;
        
        // Break out if we've reached an end game (win or draw)
        if (data.result){
          self.announceEl.text(data.result);
          window.location.hash = 'modal-two';
          bus.trigger('appView:endGame');
        } else{
          self.getComputerMove();
        }
      });
    },

    // Fetch the computers next move
    getComputerMove: function(){
      var self = this;

      $.get('/play', function(data){
        self.$el.find('.cell'+data.position).text(self.gameInit.computer);
        this.total_moves = ++this.total_moves;

        // Break out if we've reached an end game (win or draw)
        if (data.result){
          self.announceEl.text(data.result);
          window.location.hash = 'modal-two';
          bus.trigger('appView:endGame');
        }
      });
    },

    restartGame: function(){
      window.location='/restart';
    }

  });
  
  /**
   * Init collection of cells
   */
  var Board = new Backbone.Collection([
    {id: 1, x: 0, y: 0},
    {id: 2, x: 0, y: 1},
    {id: 3, x: 0, y: 2},
    {id: 4, x: 1, y: 0},
    {id: 5, x: 1, y: 1},
    {id: 6, x: 1, y: 2},
    {id: 7, x: 2, y: 0},
    {id: 8, x: 2, y: 1},
    {id: 9, x: 2, y: 2}
  ]);

  var bus = _({}).extend(Backbone.Events);
  var TTTView = new AppView;

  TTTView.render();

})(jQuery);
