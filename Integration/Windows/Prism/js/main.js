(function () {
 'use strict';
 var path, slash;
 path = location.href;
	if(getOS() == "MAC") {
		slash = "/";
		path = path.substring(0, path.length - 11);
	}
	if(getOS() == "WIN") {
		slash = "/";
		path = path.substring(8, path.length - 11);
	}
	//themeManager.init();
	//var cs = new CSInterface();
	
	const net = require('net');
	const server = net.createServer((socket) => {
	  socket.on('data', (data) => {
		var csInterface = new CSInterface();
		
		data = String(data)


		csInterface.evalScript(data, (result) => {
			if (result==""){
				socket.write("null");
			} else {
			socket.write(result);
			}
			
		});




		
	  });
	});
	server.maxConnections = 2;
	
	server.listen(9888);
	setTimeout(function(){
		generateButtons();
	}, 300);





 }());


function generateButtons(){
	const object = {'File Save...': 'Save Version.cmd', 'File Save comment...': 'Save Extended.cmd', 'Prism settings' : 'Settings.cmd', 'Project Browser' : 'Project Browser.cmd', 'State Manager' : 'Export.cmd'};
	var buttonHolder = document.getElementById("buttonHolder");
	var thisButton;
	var thisName;
	for (const [key, value] of Object.entries(object)){

		thisName = key
		thisButton = document.createElement("BUTTON");
		thisButton.innerHTML = thisName;
		thisButton.setAttribute("class", "scriptButton");
		//thisButton.setAttribute("id", 1);
		thisButton.setAttribute("path", "aaaa");
		thisButton.setAttribute("onclick", "buttonClick( '" + value + "' )");
		buttonHolder.appendChild(thisButton);
		var br = document.createElement("br");
		buttonHolder.appendChild(br);


	}
}

function buttonClick(buttonElement){
	
	var root = 'C:\\Prism'
	var process = require('child_process');
	var exec = process.exec;
	var cmd = 'explorer '+root+'\\Plugins\\Apps\\AfterEffects\\'+buttonElement;

	exec(cmd, function(err, stdout, stderr) {

	});

}






function getOS() {
 		var userAgent = window.navigator.userAgent,
 		platform = window.navigator.platform,
 		macosPlatforms = ['Macintosh', 'MacIntel', 'MacPPC', 'Mac68K'],
 		windowsPlatforms = ['Win32', 'Win64', 'Windows', 'WinCE'],
 		os = null;

 		if(macosPlatforms.indexOf(platform) != -1) {
 			os = "MAC";
 		} else if(windowsPlatforms.indexOf(platform) != -1) {
 			os = "WIN";
 		}
 		return os;
 	}