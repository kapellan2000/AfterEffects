
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
	const net = require('net');
	var csInterface = new CSInterface();

	const server = net.createServer((socket) => {
	  socket.on('data', (data) => {
		
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
	var debug = 1;
	if (debug === 1) {
		const object = {'File Save...': 'Save Version.cmd', 'File Save comment...': 'Save Extended.cmd', 'Prism settings' : 'Settings.cmd', 'Project Browser' : 'Project Browser.cmd', 'Export' : 'Export.cmd'};
	} else {
		
	const object = {'File Save...': 'SaveVersion', 'File Save comment...': 'SaveComment', 'Prism settings' : 'Settings', 'Project Browser' : 'ProjectBrowser', 'Export' : 'Export'};
	}
	

	var buttonHolder = document.getElementById("buttonHolder");
	var thisButton;
	var thisName;
	for (const [key, value] of Object.entries(object)){

		thisName = key
		thisButton = document.createElement("BUTTON");
		thisButton.style.color = "#8a8a8a";
		thisButton.style.background = "#232323";
		thisButton.style.width = '200px';
		thisButton.style.marginTop = "2px";
		thisButton.innerHTML = thisName;
		thisButton.setAttribute("class", "scriptButton");
		thisButton.setAttribute("path", "A");
		thisButton.setAttribute("onclick", "buttonClick( '" + value + "' )");
		buttonHolder.appendChild(thisButton);
		var br = document.createElement("br");
		buttonHolder.appendChild(br);


	}
}




function buttonClick(argumentValue){
	var debug = 1;
	if (debug === 1) {
		
		var root = 'C:\\ProgramData\\Prism2'
		var process = require('child_process');
		var exec = process.exec;
		var cmd = 'explorer '+root+'\\plugins\\AfterEffects\\Integration\\dev\\'+buttonElement;

		exec(cmd, function(err, stdout, stderr) {
		});
			
		
	} else {
		var pythonExePath = "C:/Program Files/Prism2/Python39/python.exe";
		var scriptPath = "c:/ProgramData/Prism2/plugins/AfterEffects/Scripts/Prism_AfterEffects_MenuTools.py";
		var command = '"' + pythonExePath + '" "' + scriptPath + '" "' + argumentValue + '"';
		var exec = require('child_process').exec;
		exec(command)
	}
		
}







function buttonClick(buttonElement){
	
	var root = 'c:\\Program Files\\Prism2'
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