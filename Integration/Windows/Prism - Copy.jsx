{
if (SERVER == null) {
	var SERVER = (function(){ 
		var conn;
		
		function listen(){
			app.setTimeout(function(){
				var incoming = conn.poll();
				if (incoming){
					try {
						ans = eval(incoming.read());
						incoming.writeln(ans)
					}
					catch(err){
						incoming.writeln (err);
					}
					incoming.close();
					delete incoming
				}
				listen();
			}, 1000)
		}

		function init(){
			conn = new Socket()
			if(conn.listen(9888)){
			   listen();
			};
		else {
			alert(conn.error);
			}
		}

		function close(){
			conn.close();
			delete conn();
		}

	return {
			init: init,
			close: close,
		}
	}());

	SERVER.init()
}
function myScript(thisObj) {
          function myScript_buildUI(thisObj) {
                    var myPanel = (thisObj instanceof Panel) ? thisObj : new Window("palette", "My Panel Name", [0, 0, 300, 300], {resizeable:true});
 
                    res="group{orientation:'column',\
                              pSave: Button{text:'Save Version'},\
                              pExtended: Button{text:'Save Extended'},\
                              pExport: Button{text:'Export'},\
                              pBrowser: Button{text:'Prism Browser'},\
                              myButton: Button{text:'Settings'},\
                              connClose: Button{text:'Close'},\
                              },\
                    }"

                    closeConn="group{orientation:'column',\
                              clButton: Button{text:'Close'},\
                              },\
                    }"

                    //Add resource string to panel
                    myPanel.grp = myPanel.add(res);

                    var myBtn = myPanel.grp.pBrowser;
                    
                    myBtn.onClick = function(){

                        cmd = 'explorer C:\\Prism\\Plugins\\Apps\\AfterEffects\\Prism.cmd' ;
                        system.callSystem(cmd)
                        }

                    var scClose = myPanel.grp.connClose;
                    scClose.onClick = function(){
						close()
                        }

                    //Setup panel sizing and make panel resizable
                    myPanel.layout.layout(true);
                    myPanel.grp.minimumSize = myPanel.grp.size;
                    myPanel.layout.resize();
                    myPanel.onResizing = myPanel.onResize = function () {this.layout.resize();}
 
                    return myPanel;
          }
 
 
          var myScriptPal = myScript_buildUI(thisObj);
 
 
          if ((myScriptPal != null) && (myScriptPal instanceof Window)) {
                    myScriptPal.center();
                    myScriptPal.show();
                    }
          }
 
 
          myScript(this);
}
 