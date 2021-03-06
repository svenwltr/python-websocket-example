		//Funktion zur Ausgabe einer neuen Nachricht im Chat-Fenster    
            function ausgabe(user, nachricht){
                $("#ausgabe1").append("<div><span style='font-weight: bold'>" + user + "</span>: " + nachricht + "</div>");
                $("#ausgabe1").scrollTop($("#ausgabe1").prop("scrollHeight"));
                }
				
        //Aktualisieren der Buddylist    
            function add_buddy(buddy){
                $("#buddylist").empty();
                for (var i = 0; i < buddy.length; ++i){
                    $("#buddylist").append("<div>" + buddy[i] + "</div>");
                }
            }
            
            $(document).ready(function(){
			
		//Starten der WebSocket-Verbindung, �ndern der Serveradresse
                try{
                    var host = "ws://localhost:8080/ws";  
                    var socket = new WebSocket(host);
                
                    socket.onopen = function(){
                        alert("Verbindung gestartet!");
                    }
                } catch(exception){
                    alert(exception);
                  }
            
        //Sendefunktion (Tags werden entfernt, Eingabe in JSON-Message gewandelt und Eingabe gel�scht)
                function senden(){
                    var jsObj = {
                        "event": "send",
                        "message": $("#eingabe").val(),
                    }; 
                
                    try{
                        var jsonmess = JSON.stringify(jsObj);
                        if($("#eingabe").val()!=""){
                            socket.send(jsonmess);
                        }
                    }catch(exception){alert(exception);}
               
                    $("#eingabe").val("");
               }
             
            //Reaktion auf ankommende JSON-Nachrichten (neue Nachricht, neuer User)
                socket.onmessage = function (msg){
                    var jsonmess = JSON.parse(msg.data);
                    if(jsonmess.event == "new_message"){
                        ausgabe(jsonmess.name,jsonmess.message);
                    }
                    if(jsonmess.event == "refresh_user_list"){
                        add_buddy(jsonmess.users);
                    }               
                }
             
            //Senden nach Dr�cken des Buttons               
                $("#button1").click(function(){
                     senden();
                 });
                        
             //Senden nach Dr�cken der Enter-Taste
                 $(document).keypress(function(event) {
                    if ( event.which == 13 ) {
                        senden();
                        return false;
                    }
                 });
                 
              //Abschalten der Vervollst�ndigung f�r das Eingabefeld
                $("#form1").attr('autocomplete','off');
             });
               
