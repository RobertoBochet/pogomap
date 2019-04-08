/*jshint esversion: 6 */
var googleMapsAPIScript;
var google;
var env = null;
var icons;

(()=>{
"use strict";

class Entity
{
	constructor(obj)
	{
		let self = this;

		this.id = obj.id;
		this.name = obj.name;
		this.latitude = obj.latitude;
		this.longitude = obj.longitude;
		this.image = obj.image;

		this.type = (obj.type === undefined) ? "none" : obj.type;
		this.isEligible = (obj.isEligible === undefined) ? false : Boolean(obj.isEligible);
		
		switch(this.type) {
			case "none": this.icon = Entity.icons.portal; break;
			case "pokestop": this.icon = Entity.icons.pokestop; break;
			case "gym":	this.icon = (this.isEligible) ? Entity.icons.gymEligible : Entity.icons.gym; break;
			case "unverified": this.icon = Entity.icons.unverified; break;
		}

		this.marker = new google.maps.Marker({
			position: new google.maps.LatLng(this.latitude, this.longitude),
			animation: google.maps.Animation.DROP,
			title: this.name,
			icon: this.icon,
			zIndex: this.icon.zIndex || 1
		});
		this.marker.addListener("click", () => { self.updateInfobox(); });
		this.marker.setMap(Entity.env.map);
	}
	updateInfobox()
	{console.log(this);
		Entity.env.currentEntity = this;

		Entity.env.infoSpaces.name.innerText = this.name;
		Entity.env.infoSpaces.image.src = this.image;
		
		if(key != "") {
			Entity.env.editorButtons.type.container.childNodes.forEach((o) => {o.classList.remove("selected");});
			Entity.env.editorButtons.eligible.container.childNodes.forEach((o) => {o.classList.remove("selected");});
			switch(this.type) {
				case "gym": Entity.env.editorButtons.type.gym.classList.add("selected"); break;
				case "pokestop": Entity.env.editorButtons.type.pokestop.classList.add("selected"); break;
				case "unverified": Entity.env.editorButtons.type.unverified.classList.add("selected"); break;
				case "none": Entity.env.editorButtons.type.notInPogo.classList.add("selected"); break;
			}
			switch(this.isEligible) {
				case true: Entity.env.editorButtons.eligible.eligible.classList.add("selected"); break;
				case false: Entity.env.editorButtons.eligible.notEligible.classList.add("selected"); break;
			}
		}
	}

	hide() { this.marker.setMap(null); }
	show() { this.marker.setMap(Entity.env.map); }
}
class Unverified extends Entity
{
	constructor(obj)
	{
		obj.type = "unverified";

		super(obj);
	}
}

class DataLayer
{
	constructor()
	{
		this.isHide = true;
		this.data = [];
	}
	show()
	{
		for(let i in this.data) {
			if(this.data[i].getMap() === undefined) this.data[i].setMap(DataLayer.env.map);
		}
		this.isHide = false;
	}
	hide()
	{
		for(let i in this.data) {
			if(this.data[i].getMap() !== undefined) this.data[i].setMap(undefined);
		}
		this.isHide = true;
	}
}

class Enviroment
{
	constructor()
	{
		this.mapElement = document.querySelector("#map");
		this.entities = [];
		this.currentEntity = null;

		Entity.env = this;
		DataLayer.env = this;

		this.makeMap();
		this.makeIcons();

		this.makeInfoSpaces();

		this.makeLayers();
		this.makeControlButtons();

		this.fetch();

		this.initEditor();
	}

	makeIcons()
	{
		Entity.icons = {
			portal: { 
				url: "/static/icons/portal_pink.svg",
				size: new google.maps.Size(60, 60),
				scaledSize: new google.maps.Size(60, 60),
				origin: new google.maps.Point(0, 0),
				anchor: new google.maps.Point(1/2*60, 9/10*60)
			},
			pokestop: { 
				url: "/static/icons/pokestop_blue.svg",
				size: new google.maps.Size(60, 60),
				scaledSize: new google.maps.Size(60, 60),
				origin: new google.maps.Point(0, 0),
				anchor: new google.maps.Point(1/2*60, 9/10*60),
				zIndex: 2
			},
			gym: { 
				url: "/static/icons/gym.svg",
				size: new google.maps.Size(45, 45),
				scaledSize: new google.maps.Size(45, 45),
				origin: new google.maps.Point(0, 0),
				anchor: new google.maps.Point(1/2*45, 1/2*45),
				zIndex: 3
			},
			gymEligible: { 
				url: "/static/icons/gym_gold.svg",
				size: new google.maps.Size(45, 45),
				scaledSize: new google.maps.Size(45, 45),
				origin: new google.maps.Point(0, 0),
				anchor: new google.maps.Point(1/2*45, 1/2*45),
				zIndex: 4
			},
			unverified: { 
				url: "/static/icons/question_mark.svg",
				size: new google.maps.Size(45, 45),
				scaledSize: new google.maps.Size(45, 45),
				origin: new google.maps.Point(0, 0),
				anchor: new google.maps.Point(1/2*45, 1/2*45),
				zIndex: 5
			}
		};
	}

	makeMap()
	{
		this.map = new google.maps.Map(this.mapElement, {
			zoom: 15,
			 center: new google.maps.LatLng(45.309552, 9.504114),
			 mapTypeId: google.maps.MapTypeId.HYBRID,
			zoomControl: false,
			disableDefaultUI: true,
			clickableIcons: false
		});
	}

	makeInfoSpaces()
	{
		this.infoSpaces = {};
		this.infoSpaces.imageContainer = document.createElement("div");
		this.infoSpaces.image = document.createElement("img");
		this.infoSpaces.imageContainer.classList.add("container");
		this.infoSpaces.imageContainer.append(this.infoSpaces.image);
		this.infoSpaces.image.id = "image";
		this.infoSpaces.image.src = "data:image/gif;base64,R0lGODlhAQABAIAAAAUEBAAAACwAAAAAAQABAAACAkQBADs=";
	
		this.map.controls[google.maps.ControlPosition.RIGHT_TOP].push(this.infoSpaces.imageContainer);
	
		this.infoSpaces.nameContainer = document.createElement("div");
		this.infoSpaces.name = document.createElement("div");
		this.infoSpaces.nameContainer.classList.add("container");
		this.infoSpaces.nameContainer.append(this.infoSpaces.name);
		this.infoSpaces.nameContainer.id = "nameContainer";
		this.infoSpaces.name.id = "name";
	
		this.map.controls[google.maps.ControlPosition.TOP_CENTER].push(this.infoSpaces.nameContainer);
	}

	makeControlButtons()
	{
		this.controlButtons = {};
		this.makeGridButtons();
		this.makeNestsButton();
	}
	makeGridButtons()
	{
		this.controlButtons.grids = {
			container: document.createElement("div"),
			small: document.createElement("div"),
			big: document.createElement("div")
		};
		this.controlButtons.grids.container.append(this.controlButtons.grids.big);
		this.controlButtons.grids.container.append(this.controlButtons.grids.small);
		this.controlButtons.grids.container.classList.add("buttonsContainer");
		this.controlButtons.grids.container.id = "gridButtons";
	
		this.controlButtons.grids.small.addEventListener("click", () => {
			if(this.layers.s2cells.small.isHide) this.layers.s2cells.small.show();
			else this.layers.s2cells.small.hide();
		});
		this.controlButtons.grids.big.addEventListener("click", () => {
			if(this.layers.s2cells.big.isHide) this.layers.s2cells.big.show();
			else this.layers.s2cells.big.hide();
		});
	
		this.map.controls[google.maps.ControlPosition.LEFT_TOP].push(this.controlButtons.grids.container);
	}
	makeNestsButton()
	{
		this.controlButtons.nests = {
			container: document.createElement("div"),
			nests: document.createElement("div")
		};
		this.controlButtons.nests.container.append(this.controlButtons.nests.nests);
		this.controlButtons.nests.container.classList.add("buttonsContainer");
		this.controlButtons.nests.nests.id = "nestsButton";
		this.controlButtons.nests.nests.addEventListener("click", () => {
			if(this.layers.nests.isHide) this.layers.nests.show();
			else this.layers.nests.hide();
		});
	
		this.map.controls[google.maps.ControlPosition.LEFT_TOP].push(this.controlButtons.nests.container);
	}

	makeLayers()
	{
		this.layers = {};
		this.makeGridLayers();
		this.makeNestsLayer();
	}
	makeGridLayers()
	{
		this.layers.s2cells = {};
		this.layers.s2cells.small = new DataLayer();
		this.layers.s2cells.big = new DataLayer();
	
		let s17 = new google.maps.Data();
		let s14 = new google.maps.Data();
		let s13 = new google.maps.Data();
	
		s17.setStyle({
			fillColor: 'transparent',
			strokeColor: "#AAAAAA",
			strokeWeight: 1,
			zIndex: 3
		});
		s14.setStyle({
			fillColor: 'transparent',
			strokeColor: "blue",
			strokeWeight: 3,
			zIndex: 5
		});
		s13.setStyle({
			fillColor: 'transparent',
			strokeColor: "red",
			strokeWeight: 5,
			zIndex: 10
		});
	
		s17.loadGeoJson("/static/layers/s2cells/17.geojson");
		s14.loadGeoJson("/static/layers/s2cells/14.geojson");
		s13.loadGeoJson("/static/layers/s2cells/13.geojson");
	
		this.layers.s2cells.small.data = [s14, s17];
		this.layers.s2cells.big.data = [s13];
	}
	makeNestsLayer()
	{
		this.layers.nests = new DataLayer();

		let nests = new google.maps.Data();

		nests.setStyle({
			fillColor: "green",
			fillOpacity: 0.6,
			strokeColor: "green",
			strokeWeight: 3,
			zIndex: 1
		});

		nests.loadGeoJson("/static/layers/nests.geojson");

		this.layers.nests.data = [nests];
	}

	initEditor()
	{
		let self = this;
		if(key !== "") {
			$.getJSON("/getentities/unverified/", function(data) {
				if(data.status == "ok") {
					for(let o of data.entities) {
						self.entities.push(new Unverified(o));
					}
				} else console.error("Error");
			});
			$.getJSON("/getentities/notinpogo/", function(data) {
				if(data.status == "ok") {
					for(let o of data.entities) {
						self.entities.push(new Entity(o));
					}
				} else console.error("Error");
			});
	
			this.makeEditorButtons();
		}
	}

	makeEditorButtons()
	{
		this.editorButtons = {};

		/*Type buttons*/
		this.editorButtons.type = {
			container: document.createElement("div"),
			gym: document.createElement("div"),
			pokestop: document.createElement("div"),
			unverified: document.createElement("div"),
			notInPogo: document.createElement("div")
		};
		this.editorButtons.type.container.append(this.editorButtons.type.gym);
		this.editorButtons.type.container.append(this.editorButtons.type.pokestop);
		this.editorButtons.type.container.append(this.editorButtons.type.unverified);
		this.editorButtons.type.container.append(this.editorButtons.type.notInPogo);
		this.editorButtons.type.container.classList.add("buttonsContainer");
		this.editorButtons.type.container.classList.add("buttonsContainerSelectable");
		this.editorButtons.type.container.id = "typeButtons";
		this.editorButtons.type.pokestop.addEventListener("click", ()=>{this.update({type:"pokestop"});});
		this.editorButtons.type.gym.addEventListener("click", ()=>{this.update({type:"gym"});});
		this.editorButtons.type.unverified.addEventListener("click", ()=>{this.update({type:"unverified"});});
		this.editorButtons.type.notInPogo.addEventListener("click", ()=>{this.update({type:"none"});});

		this.map.controls[google.maps.ControlPosition.RIGHT_BOTTOM].push(this.editorButtons.type.container);

		/*Eligible buttons*/
		this.editorButtons.eligible = {
			container: document.createElement("div"),
			eligible: document.createElement("div"),
			notEligible: document.createElement("div")
		};
		this.editorButtons.eligible.container.append(this.editorButtons.eligible.eligible);
		this.editorButtons.eligible.container.append(this.editorButtons.eligible.notEligible);
		this.editorButtons.eligible.container.classList.add("buttonsContainer");
		this.editorButtons.eligible.container.classList.add("buttonsContainerSelectable");
		this.editorButtons.eligible.container.id = "eligibleButtons";
		this.editorButtons.eligible.eligible.addEventListener("click", ()=>{this.update({isEligible:true});});
		this.editorButtons.eligible.notEligible.addEventListener("click", ()=>{this.update({isEligible:false});});

		this.map.controls[google.maps.ControlPosition.RIGHT_BOTTOM].push(this.editorButtons.eligible.container);
	}
	update(obj)
	{
		if(obj.type === undefined && obj.isEligible === undefined) {console.error("Error");return;}
		if(obj.type !== undefined && obj.type === this.currentEntity.type) return;
		if(obj.isEligible !== undefined && obj.isEligible === this.currentEntity.isEligible) return;

		$.getJSON("/setentities/", {
			key: key,
			id: this.currentEntity.id,
			type: ((obj.type !== undefined) ? obj.type : this.currentEntity.type),
			isEligible: + ((obj.isEligible !== undefined) ? obj.isEligible : this.currentEntity.isEligible)
		}, 
		(data) => {
			if(data.status == "ok") {
				if(data.entity.type === undefined) data.entity = new Unverified(data.entity);
				else data.entity = new Entity(data.entity);
				
				this.currentEntity.hide();
				this.entities.filter((entity) => { return this.currentEntity.id === data.entity.id });

				this.entities.push(data.entity);
				data.entity.updateInfobox();
			} else console.error("Error");
		});
	}

	fetch()
	{
		let self = this;
		$.getJSON("/getentities/inpogo/", function(data) {
			if(data.status == "ok") {
				for(let o of data.entities) {
					self.entities.push(new Entity(o));
				}
			} else console.error("Error");
		});
	}
}

window.addEventListener("load", () => {
	env = new Enviroment();
});

})();








// let foo = () => {
// 	map = new google.maps.Map(document.querySelector("#map"), {
// 		zoom: 15,
//  		center: new google.maps.LatLng(45.309552, 9.504114),
//  		mapTypeId: google.maps.MapTypeId.HYBRID,
// 		zoomControl: false,
// 		disableDefaultUI: true,
// 		clickableIcons: false
// 	});
	
// 	/*InfoSpaces*/
// 	infoSpaces.imageContainer = document.createElement("div");
// 	infoSpaces.image = document.createElement("img");
// 	infoSpaces.imageContainer.classList.add("container");
// 	infoSpaces.imageContainer.append(infoSpaces.image);
// 	infoSpaces.image.id = "image";
// 	infoSpaces.image.src = "data:image/gif;base64,R0lGODlhAQABAIAAAAUEBAAAACwAAAAAAQABAAACAkQBADs=";

// 	map.controls[google.maps.ControlPosition.RIGHT_TOP].push(infoSpaces.imageContainer);

// 	infoSpaces.nameContainer = document.createElement("div");
// 	infoSpaces.name = document.createElement("div");
// 	infoSpaces.nameContainer.classList.add("container");
// 	infoSpaces.nameContainer.append(infoSpaces.name);
// 	infoSpaces.nameContainer.id = "nameContainer";
// 	infoSpaces.name.id = "name";

// 	map.controls[google.maps.ControlPosition.TOP_CENTER].push(infoSpaces.nameContainer);

// 	/*Grids buttons*/
// 	controlButtons.grids = {
// 		container: document.createElement("div"),
// 		small: document.createElement("div"),
// 		big: document.createElement("div")
// 	};
// 	controlButtons.grids.container.append(controlButtons.grids.big);
// 	controlButtons.grids.container.append(controlButtons.grids.small);
// 	controlButtons.grids.container.classList.add("buttonsContainer");
// 	controlButtons.grids.container.id = "gridButtons";

// 	controlButtons.grids.small.addEventListener("click", () => {
// 		if(layers.s2cells.small.isHide) layers.s2cells.small.show();
// 		else layers.s2cells.small.hide();
// 	});
// 	controlButtons.grids.big.addEventListener("click", () => {
// 		if(layers.s2cells.big.isHide) layers.s2cells.big.show();
// 		else layers.s2cells.big.hide();
// 	});

// 	map.controls[google.maps.ControlPosition.LEFT_TOP].push(controlButtons.grids.container);

// 	/*Grids buttons*/
// 	controlButtons.nests = {
// 		container: document.createElement("div"),
// 		nests: document.createElement("div")
// 	};
// 	controlButtons.nests.container.append(controlButtons.nests.nests);
// 	controlButtons.nests.container.classList.add("buttonsContainer");
// 	controlButtons.nests.nests.id = "nestsButton";
// 	controlButtons.nests.nests.addEventListener("click", () => {
// 		if(layers.nests.isHide) layers.nests.show();
// 		else layers.nests.hide();
// 	});

// 	map.controls[google.maps.ControlPosition.LEFT_TOP].push(controlButtons.nests.container);


// 	/*Grids layers*/
// 	layers.s2cells = {};
// 	layers.s2cells.small = new DataLayer();
// 	layers.s2cells.big = new DataLayer();

// 	let s17 = new google.maps.Data();
// 	let s14 = new google.maps.Data();
// 	let s13 = new google.maps.Data();

// 	s17.setStyle({
// 		fillColor: 'transparent',
// 		strokeColor: "#AAAAAA",
// 		strokeWeight: 1,
// 		zIndex: 1
// 	});
// 	s14.setStyle({
// 		fillColor: 'transparent',
// 		strokeColor: "green",
// 		strokeWeight: 3,
// 		zIndex:5
// 	});
// 	s13.setStyle({
// 		fillColor: 'transparent',
// 		strokeColor: "red",
// 		strokeWeight: 5,
// 		zIndex: 10
// 	});

// 	s17.loadGeoJson("/layers/s2cells/17.geojson");
// 	s14.loadGeoJson("/layers/s2cells/14.geojson");
// 	s13.loadGeoJson("/layers/s2cells/13.geojson");

// 	layers.s2cells.small.data = [s14, s17];
// 	layers.s2cells.big.data = [s13];


// 	/*Nests layers*/
// 	layers.nests = new DataLayer();

// 	let nests = new google.maps.Data();

// 	nests.setStyle({
// 		fillColor: "green",
// 		fillOpacity: 0.6,
// 		strokeColor: "green",
// 		strokeWeight: 3,
// 		zIndex:5
// 	});

// 	nests.loadGeoJson("/layers/nests.geojson");

// 	layers.nests.data = [nests];

	
// 	/*Initial fetch*/
// 	$.getJSON("/getentities.php?type=inpogo", function(data) {
// 		if(data.status == "ok") {
// 			for(let o of data.entities) {
// 				entities.push(new Entity(o));
// 			}
// 		} else console.error("Error");
// 	});

// 	/*Edit mode*/
// 	if(key !== "") {
// 		/*Fetch portals*/
// 		$.getJSON("/getentities.php?type=unverified", function(data) {
// 			if(data.status == "ok") {
// 				for(let o of data.entities) {
// 					entities.push(new Unverified(o));
// 				}
// 			} else console.error("Error");
// 		});
// 		$.getJSON("/getentities.php?type=notinpogo", function(data) {
// 			if(data.status == "ok") {
// 				for(let o of data.entities) {
// 					entities.push(new Entity(o));
// 				}
// 			} else console.error("Error");
// 		});

// 		/*Update*/
// 		let update = (obj) => {
// 			if(obj.type === undefined && obj.isEligible === undefined) {console.error("Error");return;}
// 			if(obj.type !== undefined && obj.type === currentEntity.type) return;
// 			if(obj.isEligible !== undefined && obj.isEligible === currentEntity.isEligible) return;

// 			$.getJSON("/setentities.php", {
// 				key: key,
// 				id: currentEntity.id,
// 				type: ((obj.type !== undefined)?obj.type:currentEntity.type),
// 				isEligible: + ((obj.isEligible !== undefined)?obj.isEligible:currentEntity.isEligible)
// 			}, 
// 			(data) => {
// 				if(data.status == "ok") {
// 					if(data.entity.type === undefined) data.entity = new Unverified(data.entity);
// 					else data.entity = new Entity(data.entity);
					
// 					currentEntity.hide();
// 					entities.filter((entity) => { return currentEntity.id === data.entity.id });

// 					entities.push(data.entity);
// 					data.entity.updateInfobox();
// 				} else console.error("Error");
// 			});
// 		};

// 		/*Type buttons*/
// 		editorButtons.type = {
// 			container: document.createElement("div"),
// 			gym: document.createElement("div"),
// 			pokestop: document.createElement("div"),
// 			unverified: document.createElement("div"),
// 			notInPogo: document.createElement("div")
// 		};
// 		editorButtons.type.container.append(editorButtons.type.gym);
// 		editorButtons.type.container.append(editorButtons.type.pokestop);
// 		editorButtons.type.container.append(editorButtons.type.unverified);
// 		editorButtons.type.container.append(editorButtons.type.notInPogo);
// 		editorButtons.type.container.classList.add("buttonsContainer");
// 		editorButtons.type.container.classList.add("buttonsContainerSelectable");
// 		editorButtons.type.container.id = "typeButtons";
// 		editorButtons.type.pokestop.addEventListener("click", ()=>{update({type:"pokestop"});});
// 		editorButtons.type.gym.addEventListener("click", ()=>{update({type:"gym"});});
// 		editorButtons.type.unverified.addEventListener("click", ()=>{update({type:"unverified"});});
// 		editorButtons.type.notInPogo.addEventListener("click", ()=>{update({type:"none"});});

// 		map.controls[google.maps.ControlPosition.RIGHT_BOTTOM].push(editorButtons.type.container);

// 		/*Eligible buttons*/
// 		editorButtons.eligible = {
// 			container: document.createElement("div"),
// 			eligible: document.createElement("div"),
// 			notEligible: document.createElement("div")
// 		};
// 		editorButtons.eligible.container.append(editorButtons.eligible.eligible);
// 		editorButtons.eligible.container.append(editorButtons.eligible.notEligible);
// 		editorButtons.eligible.container.classList.add("buttonsContainer");
// 		editorButtons.eligible.container.classList.add("buttonsContainerSelectable");
// 		editorButtons.eligible.container.id = "eligibleButtons";
// 		editorButtons.eligible.eligible.addEventListener("click", ()=>{update({isEligible:true});});
// 		editorButtons.eligible.notEligible.addEventListener("click", ()=>{update({isEligible:false});});

// 		map.controls[google.maps.ControlPosition.RIGHT_BOTTOM].push(editorButtons.eligible.container);
// 	}

// 	/*User position*/
// 	if (navigator.geolocation) {
// 		navigator.geolocation.getCurrentPosition(function(position) {
// 			var pos = {
// 				lat: position.coords.latitude,
// 				lng: position.coords.longitude
// 			};
// 			map.setCenter(pos);
// 		});
// 	}
// };