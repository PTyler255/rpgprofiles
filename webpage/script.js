//On Load
window.onload = loadPlayers();

function authAndLoad() {
	document.querySelector("#foo").disbled = true;
	document.querySelector("#bar").disabled = true;
	document.querySelector("#form").style.display = "none";
	document.querySelectorAll("h2")[0].style.display = "none";
	document.querySelectorAll("h2")[1].style.display = "none";
	document.querySelector("#signreg").style.display = "block";
	document.querySelector("#signform").style.display = "none";
}

//Buttons
document.querySelector("#foo").onclick = function() {
	var form = getForm();
	clearForm();
	addPlayerToServer(form);
	removeAllChildNodes(document.querySelector("#content"));
	loadPlayers();
}
document.querySelector("#bar").onclick = function() {
	var form = getForm();
	var ides = document.querySelector("#ide").value;
	var button = document.querySelector("#bar");
	clearForm()
	updatePlayerOnServer(form, "/"+ides);
	removeAllChildNodes(document.querySelector("#content"));
	document.querySelector("#foo").style.display = "block";
	button.style.dipslay = "none";
}

document.querySelector("#regbutt").onclick = function() {
	var from = getReg();
	clearReg();
	if (from['rpw'] == from['cpw']) {
		addUserToServer(from);
	} else if (from['rwp'] != from['cpw']) {
		document.querySelector("#signreg").querySelector("p").innerHTML = "Passwords must match";
	}
}

document.querySelector("#signbutt").onclick = function() {
	var from = getSign();
	clearSign();
	authenticateUser(from);
}

document.querySelector("#reg").onclick = function() {
	document.querySelector("#regform").style.display = "grid";
	document.querySelector("#signform").style.display = "none";
	document.querySelector("#reg").style.backgroundColor = "#FBE4B1";
	document.querySelector("#sign").style.backgroundColor = "";
}

document.querySelector("#sign").onclick = function() {
	document.querySelector("#signform").style.display = "grid";
	document.querySelector("#regform").style.display = "none";
	document.querySelector("#reg").style.backgroundColor = "";
	document.querySelector("#sign").style.backgroundColor = "#FBE4B1";
}
//Base Functions
function addContent(dict, asdf) {
	var nameField = document.createTextNode(dict["name"]);
	var classField = document.createTextNode(dict["class"]);
	var levelField = document.createTextNode(dict["level"]);
	var moneyField = document.createTextNode("$ = " + dict["money"]);
	var resourceField = document.createTextNode("Res.: " + dict["resource"]);
	var notesField = document.createTextNode(dict["notes"]);
	var head = document.createElement("div");
	head.className = "head";
	var side = document.createElement("div");
	side.className = "side";
	var nameC = document.createElement("h2");
	var classC = document.createElement("h3");
	var levelC = document.createElement("h3");
	var moneyC = document.createElement("p");
	var resourceC = document.createElement("p");
	var notesC = document.createElement("p");
	asdf.className = "play";
	nameC.appendChild(nameField);
	nameC.className = "name";
	classC.appendChild(classField);
	classC.className = "class";
	levelC.appendChild(levelField);
	levelC.className = "level";
	head.appendChild(nameC);
	head.appendChild(classC);
	head.appendChild(levelC);
	moneyC.appendChild(moneyField);
	moneyC.className = "money";
	resourceC.appendChild(resourceField);
	resourceC.className = "resource";
	side.appendChild(moneyC);
	side.appendChild(resourceC);
	notesC.appendChild(notesField);
	notesC.className = "notes";
	asdf.appendChild(head);
	asdf.appendChild(side);
	asdf.appendChild(notesC);
}

function logIn() {
	document.querySelector("#foo").disbled = false;
	document.querySelector("#bar").disabled = false;
	document.querySelector("#form").style.display = "grid";
	document.querySelectorAll("h2")[0].style.display = "block";
	document.querySelectorAll("h2")[1].style.display = "block";
	document.querySelector("#signreg").style.display = "none";
}

function clearForm() {
	document.querySelector("#name").value = '';
	document.querySelector("#class").value = '';
	document.querySelector("#level").value = '';
	document.querySelector("#money").value = '';
	document.querySelector("#resource").value = '';
	document.querySelector("#notes").value = '';
}

function getForm() {
	var name = document.querySelector("#name").value;
	var clss = document.querySelector("#class").value;
	var level = document.querySelector("#level").value;
	var money = document.querySelector("#money").value;
	var reso = document.querySelector("#resource").value;
	var notes = document.querySelector("#notes").value;
	var dict = {};
	dict["name"] = name;
	dict["class"] = clss;
	dict["level"] = level;
	dict["money"] = money;
	dict["resource"] = reso
	dict["notes"] = notes;
	return dict;
}

function getReg() {
	var fname = document.querySelector("#fname").value;
	var lname = document.querySelector("#lname").value;
	var rem = document.querySelector("#rem").value;
	var rpw = document.querySelector("#rpassword").value;
	var cpw = document.querySelector("#cpass").value;
	var dict = {};
	dict["fname"] = fname;
	dict['lname'] = lname;
	dict['email'] = rem;
	dict['rpw'] = rpw;
	dict['cpw'] = cpw;
	return dict;
}

function getSign() {
	var sem = document.querySelector("#sem").value;
	var spw = document.querySelector("#spass").value;
	var dict = {};
	dict['email'] = sem;
	dict['spw'] = spw;
	return dict;
}

function clearReg() {
	document.querySelector("#fname").value = '';
	document.querySelector("#lname").value = '';
	document.querySelector("#rem").value = '';
	document.querySelector("#rpassword").value = '';
	document.querySelector("#cpass").value = '';
	document.querySelector("#signreg").querySelector("p").innerHTML = "";
}

function clearSign() {
	document.querySelector("#sem").value = '';
	document.querySelector("#spass").value = '';
	document.querySelector("#signreg").querySelector("p").innerHTML = "";
}

function inputForm(dict) {
	document.querySelector("#ide").value = dict["id"];
	document.querySelector("#name").value = dict["name"];
	document.querySelector("#class").value = dict["class"];
	document.querySelector("#level").value = dict["level"];
	document.querySelector("#money").value = dict["money"];
	document.querySelector("#resource").value = dict["resource"];
	document.querySelector("#notes").value = dict["notes"];
}


function removeAllChildNodes(parent) {
	while (parent.firstChild) {
		parent.removeChild(parent.firstChild);
	}
}

//Fetch interaction
//POST
function addPlayerToServer(info) {
	var data = "name=" + encodeURIComponent(info["name"]) + "&class=" + encodeURIComponent(info["class"]) + "&level=" + encodeURIComponent(info["level"]) + "&money=" + encodeURIComponent(info["money"]) + "&resource=" + encodeURIComponent(info["resource"]) + "&notes=" + encodeURIComponent(info["notes"]) + "&";
	fetch("https://server-side-characters.herokuapp.com/PLAYERS", {
		//fetch options here
		method: "POST", //post method
		body: data,//request body with data
		credentials: "include",
		headers: { 
			"Content-Type" : "application/x-www-form-urlencoded"
		}//headers (to describe the body)
	}).then(function(response) {
		console.log(response)//the server has resopnded here.
		loadPlayers();

	});
}

function addUserToServer(info) {
	var data = "fname=" + encodeURIComponent(info["fname"]) + "&lname=" + encodeURIComponent(info["lname"]) + "&email=" + encodeURIComponent(info["email"]) + "&password=" + encodeURIComponent(info["rpw"]) + "&";
	fetch("https://server-side-characters.herokuapp.com/USERS", {
		//fetch options here
		method: "POST", //post method
		body: data,//request body with data
		credentials: "include",
		headers: { 
			"Content-Type" : "application/x-www-form-urlencoded"
		}//headers (to describe the body)
	}).then(function(response) {
		if (response.status == 404 || response.status == 401) {
			document.querySelector("#signreg").querySelector("p").innerHTML = "User email already exists.";
		} else if (response.status == 201 ){
			document.querySelector("#signreg").querySelector("p").innerHTML = "User created.";
			document.querySelector("#signform").style.display = "block";
			document.querySelector("#regform").style.display = "none";
		} else {
			document.querySelector("#signreg").querySelector("p").innerHTML = "Something went wrong";
		 }
	});
}

function authenticateUser(info) {
	var login = "email=" + encodeURIComponent(info["email"]) + "&password=" + encodeURIComponent(info["spw"]) + "&";
	fetch("https://server-side-characters.herokuapp.com/SESSIONS", {
		//fetch options here
		method: "POST", //post method
		body: login,//request body with data
		credentials: "include",
		headers: { 
			"Content-Type" : "application/x-www-form-urlencoded"
		}//headers (to describe the body)
	}).then(function(response) {
		if (response.status == 401) {
			document.querySelector("#signreg").querySelector("p").innerHTML = "Incorrect email or password.";
		} else if (response.status == 201) {
			loadPlayers();
		}
	});
}


//PUT
function updatePlayerOnServer(info, id) {
	var data = "name=" + encodeURIComponent(info["name"]) + "&class=" + encodeURIComponent(info["class"]) + "&level=" + encodeURIComponent(info["level"]) + "&money=" + encodeURIComponent(info["money"]) + "&resource=" + encodeURIComponent(info["resource"]) + "&notes=" + encodeURIComponent(info["notes"]) + "&";
	fetch("https://server-side-characters.herokuapp.com/PLAYERS" + id, {
		//fetch options here
		method: "PUT", //post method
		body: data,//request body with data
		credentials: "include",
		headers: { 
			"Content-Type" : "application/x-www-form-urlencoded"
		}//headers (to describe the body)
	}).then(function(response) {
		console.log(response)//the server has resopnded here.
		if (response.status == 200){
			loadPlayers()
		}
	});
}
//GET
function loadPlayers() {
	fetch("https://server-side-characters.herokuapp.com/PLAYERS", {credentials: "include"}).then(function(response){
	//here the server has now responded
		if (response.status != 401) {
			removeAllChildNodes(document.querySelector("#content"));
			logIn();
			response.json().then(function(dataFromServer) {
				var players = dataFromServer;
				players.forEach(function (element) {
					var player = element;
					var ide = player["id"];
					var abcd = document.createElement("div");
					addContent(player, abcd);
					var del  = document.createTextNode("X");
					var edit = document.createTextNode("E");
					var delbutt = document.createElement("button");
					var editbutt = document.createElement("button");
					delbutt.appendChild(del);
					editbutt.appendChild(edit);
					delbutt.onclick = function() {
						if (true == confirm("Are you sure you wish to delete " + player["name"] + "?")){
							removeAllChildNodes(document.querySelector("#content"));
							deletePlayer(ide);
							loadPlayers();
						}
					}	
					editbutt.onclick = function() {
						inputForm(player);
						var button = document.querySelector("#foo");
						button.style.display = "none";
						document.querySelector("#bar").style.display = "block";
					}
					document.querySelector("#bar").style.display = "none";
					var headr = abcd.querySelector(".head");
					var buttons = document.createElement("span");
					buttons.appendChild(editbutt);
					buttons.appendChild(delbutt);
					headr.appendChild(buttons);
					document.querySelector("#content").appendChild(abcd);
					//loop over the data and display in the dom
					//PY for element in array
				});
			});
		} else {
				authAndLoad();
		}
	});
};


//DELETE
function deletePlayer(id) {
	fetch("https://server-side-characters.herokuapp.com/PLAYERS/" + id, {
		method: "DELETE",
		credentials: "include"
	}).then(function(response) {
		if (response.status == 200){
			removeAllChildNodes(document.querySelector("#content"));
			loadPlayers();
		}
	})
}

