// filterMgt.js
var filter = new Array(); 

function addFilterOptions(node)
{
	 var inversion = {
             identifier: 'decision',
             label: 'name',
             items: [{
                 decision: '0',
                 name: 'NICHT'
                 
             },
             {
                 decision: '1',
                 name: " "
             }]
         }
	 
	 var bereich = {
			 identifier: "id",
			 label: "name",
			 items: [{
			  id:"0",
			  name:"Funktion"
			 }]
	 }
	 
	 var bereichWerte = {
			 identifier: "id",
			 label: "name",
			 items: [{
				 id:"0",
				 name:"Management"
			 },
			 {
				 id:"1",
				 name:"Si-Beauftragter"
			 },
			 {
				 id:"2",
				 name:"Wartung"
			 },
			 {
				 id:"3",
				 name:"Benutzer"
			 },
			 {
				 id:"4",
				 name:"Revision"
			 }]
	 }
	 
	 var link = {
			 identifier: "id",
			 label: "name",
			 items: [{
				 id:"0",
				 name:"ODER"
			 },
			 {
				 id:"1",
				 name:"UND"
			 },
			 {
				 id:"2",
				 name:" "
			 }]
	 }
	 require(["dojo/data/ItemFileWriteStore", "dojo/data/ItemFileReadStore", "dijit/form/ComboBox", "dijit/form/Button"], function (ItemFileWriteStore, ItemFileReadStore, ComboBox, Button){
	 var options = new ItemFileWriteStore({
         data: {
           identifier : "name", items : [
             {name : "A"},
             {name : "B"},
             {name : "C"}
           ]
         }
       });

	var invStore = new ItemFileReadStore({data:inversion});
	var bereichStore = new ItemFileReadStore({data:bereich});
	var werteStore = new ItemFileReadStore ({data:bereichWerte});
	var linkStore = new ItemFileReadStore ({data:link});
		
	node.appendChild(new ComboBox({name: "inverse", value: " ", store: invStore, searchAttr: "name", style:"width:75px"},"inverse").domNode);
	node.appendChild(new ComboBox({name: "bereich", value: "Funktion", store: bereichStore, searchAttr: "name", style:"width:150px"},"bereich").domNode);
	node.appendChild(new ComboBox({name: "wert", value: "Management", store: werteStore, searchAttr: "name"},"wert").domNode);
	node.appendChild(new ComboBox({name: "link", value: "UND", store: linkStore, searchAttr: "name", style:"width:75px"},"link").domNode);
	node.appendChild(new Button({label:"X2"}).domNode);
	var myDijit = new ComboBox({
        store : options
      });
    node.appendChild(myDijit.domNode);
	node.innerHTML += "<br>";
	});
}
// functions.lib.js
var lastChecklistItem = null;

function addTab2Lesebereich()
{
	require(["dijit/layout/ContentPane"], function(ContentPane) {
	lesebereichTabsNum++;
	var newTab = new ContentPane({title:"Tab " + lesebereichTabsNum, closable:"true"});

	lesebereich.addChild(newTab);
	lesebereich.selectChild(newTab);
	return newTab;
	});
}

function resizeFont(element,factor)
{
	size = element.style.fontSize;
	
	if (size == "")		
		size = 0.7;		
	else
		size = parseFloat(element.style.fontSize.replace('em',''));
	size += factor;
	
	if(size > 0.5 && size < 10)
		element.style.fontSize = size.toFixed(1)+'em';
	
} 

function getURL(url)
{
	var tmpUrl = "";

	if (journal.entries.length > 0)
	{	
		require(["dojo/cookie"], function (cookie) {
		var _tmp = journal.toString();
		
		if (_tmp.indexOf("\n") > 0)
			_tmp = _tmp.replace(/\n/g,"<br>");
		if (_tmp.indexOf("\r") > 0)
			_tmp = _tmp.replace(/\r/g,"");
		
		cookie("journal", _tmp,{expires:10});	
		
		var jetzt = new Date();
		cookie("zeit", jetzt.getTime(),{expires:10});	
		
		journal.entries = new Array();
		});
	}
	return url+tmpUrl;
}

function check4LeftClick (element, dom)
{
	require(["dojo/dom-class"], function (domClass) {
	if (lastChecklistItem != null)
	{
		var _selection = lesebereich.selectedChildWidget.title.split(":");
		_selection = _selection[0];		
		if (domClass.contains(lastChecklistItem.id,"checklist_comment"))
		{
			if (dom.byId(lastChecklistItem.id).value == "")
				journal.addEntry("comment", '{"'+_selection+'":{"'+lastChecklistItem.id+'":"#leer#"}}');
			else
				journal.addEntry("comment", '{"'+_selection+'":{"'+lastChecklistItem.id+'":"'+formatString4XML(lastChecklistItem.value)+'"}}');
		}
		else
		{
			var _id = lastChecklistItem.id;
			_tmp =  _id.split("_");
			var _old = _tmp[2];
			var _new = _old.split("-");
			_new = _new[1];
			journal.addEntry("commentRatio",'{"'+_selection+'":{"'+_id.replace(_old,_new)+'":"'+lastChecklistItem.value+'"}}');
		}
		lastChecklistItem = null;
	}

	if (element.hasAttribute("id"))	
		if (domClass.contains(element.id,"checklist_comment") || domClass.contains(element.id,"checklist_radio"))
		{
			lastChecklistItem = element;
		}
	});
}

function formatString4XML(str)
{
	str = str.replace("&","&amp;");
	
	return str;
}

function openHelp ()
{
	var popupWindow = window.open('help.html', "Hilfe Sicherheitshandbuch", "width=700,height=900,scrollbars=no,resizable=yes");
	popupWindow.focus();
}

function openHelp (reference)
{
	var src = "help.html";
	
	if (typeof(reference) != 'undefined')
		src += "#"+reference;
	
	var popupWindow = window.open(src,"Hilfe","width=700,height=900,left=300,top=200,scrollbars=no,resizable=yes");
	popupWindow.focus();
}

function openPrint()
{
	require(["dojo/dom"], function(dom){
		var popupWindow = window.open('', "Zweitfenster", "width=933,height=700,scrollbars=yes,resizable=yes");
		popupWindow.document.write("<link rel='stylesheet' type='text/css' href='css/main.css'/> <p><a href='javascript:window.print()'>Diese Seite drucken</a></p>"+dom.byId(lesebereich.selectedChildWidget.id).innerHTML);
		//popupWindow.window.print();
		popupWindow.focus();
	});
}

function isString (input)
{
	return typeof(input) == 'string';
}
//genContextMenu.lib.js
var nlContextMenuCostumeItems;
var contextMenu;

function initCustomContext ()
{
	require(["dojo/query", "dijit/Menu"], function(query, Menu){
	nlContextMenuCostumeItems = new query.NodeList();
	contextMenu = new Menu({contextMenuForWindow: "true"});
	});
}

function clearCustomContext ()
{
	require(["dojo/query"], function(query){
	nlContextMenuCostumeItems.forEach(function(node, index, array){
		node.destroy();
	});
	nlContextMenuCostumeItems = new query.NodeList();
	});
}

function callContextOnDivClass(node, registry)
{
	require(["dojo/dom-class"], function (domClass) {
	if (nlContextMenuCostumeItems.length != 0)
		clearCustomContext();
	
	if (node == null)
		return false;

	if (domClass.contains(node,"chapter"))
	{
/*		//Kapitel hinzufügen
		var contextElement = new dijit.MenuItem ({id: "costumMenuItem_chapter1", iconClass:"dijitEditorIcon dijitEditorIconCopy", label:"Irgendwas <b>Kapitel</b> spezifisches", title:"Kapitel spezifisches"});
		contextMenu.addChild(contextElement);
		contextElement.on("click",function(){ alert('Da koennte etwas Kapitel spezifisches passieren!'); });
		nlContextMenuCostumeItems.push(contextElement);
		
		addContext4siha();
		contextMenu.startup();
*/
		return true;
	}
	if (domClass.contains(node,"section"))
	{
/*
		node.style.border ="1px solid green";
		//dojo.style(node,{border:"1px solid green"});
		var contextElement = new dijit.MenuItem ({id: "costumMenuItem_section1", iconClass:"dijitEditorIcon dijitEditorIconCopy", label:"Irgendwas <b>Abschnitt</b> spezifisches", title:"Abschnitt spezifisches"});
		
		contextMenu.addChild(contextElement);
		contextElement.on("click",function(){ alert('Da koennte etwas Abschnitt spezifisches passieren!'); });

		nlContextMenuCostumeItems.push(contextElement);

		addContext4siha();
		contextMenu.startup();
*/
		return true;
	}
	
	if (domClass.contains(node,"topic"))
	{
		node.style.backgroundColor = "#e6ffff";

		addContext4siha(node.getAttribute("id"));
		contextMenu.startup();

		return true;
	}
	
	if (domClass.contains(node,"dijitTreeRow")) //dijitTreeLabel dijitTreeLabelActive
	{
		var tmpNode = node;
		var tmpID = true;
		
		while (tmpID || tmpID == null || tmpID == "")
		{
			while (tmpNode.hasAttribute("id") == null || tmpNode.tagName != "DIV")
				tmpNode = tmpNode.parentNode;
			tmpID = tmpNode.getAttribute("id");
			if (tmpID == null || tmpID == "")
				tmpNode = tmpNode.parentNode;
			else
				break;
		}
		
		tmpNode = registry.byId(tmpID);
		var label = tmpNode.label;
		
		var tmpItem;
		theJSON.fetch({
			query: {"title":label},
			queryOptions: {deep:true}, 
			onItem: function(item, request){
				tmpItem = item;
			},
			onError: function(error) {
				alert("Fehler: "+error);
			}
		});
		
		if (theJSON.getValue(tmpItem,"type") == "auswahl"){
			addContext4Selection(tmpNode, theJSON.getIdentity(tmpItem));
			return true;
		}
	}

	if (node.id == "sihaTree")
	{
		addContext4sihatree();
		contextMenu.startup();
		
		return true;
	}

	return callContextOnDivClass(node.parentNode, registry);
	});
}

function addContext4siha (nodeID)
{
	require(["dijit/MenuItem", "dijit/Menu", "dijit/PopupMenuItem"], function(MenuItem, Menu, PopupMenuItem) {
	var contextSubMenu4Siha = new Menu();
		var ceSiha0 = new MenuItem ({id: "costumMenuItem_ceSiha0", iconClass:"dijitEditorIcon dijitEditorIconCopy", label:"Zu neuer Auswahl hinzuf&uuml;gen", title:"Es wird eine Auswahl angelegt in die Ihre ausgewaehlten Elemente eingefuegt werden."});
		ceSiha0.on("click",function() {
			var newSel = addSelection();
			listStore[getListindexById(newSel)].addUID("101");
			addUIDtoSelection(newSel, nodeID);
			}
		);
		contextSubMenu4Siha.addChild(ceSiha0);
		/* **** */
		var i;
		for (i=0; i < listStore.length; i++)
		{
			if(listStore[i] == undefined)
				continue;
			var _tmp = new MenuItem ({id: "costumMenuItem_ceSiha_"+i, iconClass:"dijitEditorIcon dijitEditorIconCopy", label:listStore[i].id, title:"Zur Auswahl "+listStore[i].id+" hinzufuegen"});
			contextSubMenu4Siha.addChild(_tmp);
			_tmp.on("click", function(evt) {
				addUIDtoSelection(evt.target.innerHTML, nodeID);
			});
			
			nlContextMenuCostumeItems.push(_tmp);
		}
		/* **** */
	
	//Trennung für chapter/section/topic Einträge
	//var ceSihaSep1 = new dijit.MenuSeparator();
	//contextMenu.addChild(ceSihaSep1);
	var ceSihaPopUp1 = new PopupMenuItem({label:"Einer Auswahl hinzuf&uuml;gen",popup:contextSubMenu4Siha});
	contextMenu.addChild(ceSihaPopUp1);

	//nlContextMenuCostumeItems.push(ceSihaSep1);
	nlContextMenuCostumeItems.push(ceSiha0);
	nlContextMenuCostumeItems.push(ceSihaPopUp1);
	/* ************************************** */
	});
}

function addContext4Selection(node, itemID)
{
	require(["dijit/MenuItem", "dijit/Menu", "dijit/PopupMenuItem"], function(MenuItem, Menu, PopupMenuItem) {
	var ce1 = new MenuItem ({id: "costumMenuItem_selection1", iconClass:"dijitEditorIcon dijitEditorIconCopy", label:"Umbenennen", title:"Auswahl umbenennen"});
	contextMenu.addChild(ce1);
	ce1.on("click",function(){
		renameSelection(itemID); 
	});
	nlContextMenuCostumeItems.push(ce1);
	/* **************** */
	
	var contextSubMenuSave = new Menu();
		var ce2 = new MenuItem ({id: "costumMenuItem_selection2", iconClass:"dijitEditorIcon dijitEditorIconCopy", label:"... als PDF", title:"Auswahl als PDF speichern"});
		contextSubMenuSave.addChild(ce2);
		ce2.on("click",function(){
			saveSelection(itemID,"pdf");
		});
		var ce3 = new MenuItem ({id: "costumMenuItem_selection3", iconClass:"dijitEditorIcon dijitEditorIconCopy", label:"... als XML", title:"Auswahl als XML speichern"});
		contextSubMenuSave.addChild(ce3);
		ce3.on("click",function(){
			saveSelection(itemID,"xml");
		});
	var ceSihaPopUpSave = new PopupMenuItem({label:"Auswahl speichern als ...",popup:contextSubMenuSave});
	contextMenu.addChild(ceSihaPopUpSave);

	nlContextMenuCostumeItems.push(ce2);
	nlContextMenuCostumeItems.push(ce3);
	nlContextMenuCostumeItems.push(ceSihaPopUpSave);
	/* ************* */
	
	var contextSubMenuTransform = new Menu();
		var ce4 = new MenuItem({id: "costumMenuItem_selection4", iconClass:"dijitEditorIcon dijitEditorIconCopy", label:"Checkliste", title:"Checkliste aus Auswahl generieren"});
		contextSubMenuTransform.addChild(ce4);
		ce4.on("click",function(){
			selectionToChecklist(itemID);
		});
	var ceSihaPopUpTransform = new PopupMenuItem({label:"Auswahl zu ...",popup:contextSubMenuTransform});
	contextMenu.addChild(ceSihaPopUpTransform);
	
	nlContextMenuCostumeItems.push(ce4);
	nlContextMenuCostumeItems.push(ceSihaPopUpTransform);
	/**************************/
	
	var ce5 = new MenuItem ({id: "costumMenuItem_selection5", iconClass:"dijitEditorIcon dijitEditorIconCopy", label:"L&ouml;schen", title:"Auswahl loeschen"});
	contextMenu.addChild(ce5);
	ce5.on("click",function(){
		delSelection(itemID);
	});
	nlContextMenuCostumeItems.push(ce5);
	/**************************/
	
	contextMenu.startup();
	});
}

function addContext4sihatree()
{
	require(["dijit/MenuItem"], function (MenuItem) {
	var ce1 = new MenuItem ({id: "costumMenuItem_sihatree1", iconClass:"dijitEditorIcon dijitEditorIconCopy", label:"Neue Auswahl hinzuf&uuml;gen", title:"Neue Auswahl hinzufuegen"});
	contextMenu.addChild(ce1);
	ce1.on("click",function(){
		var newSel = addSelection();
		listStore[getListindexById(newSel)].addUID("101");
	});
	nlContextMenuCostumeItems.push(ce1);
	/* *********************** */
	});
}

// journal.class.js
function Journal () {
	this.entries = new Array();
}

/* *** SETTERS *** */

/* *** GETTERS *** */



/* *** Methods *** */

Journal.prototype.addEntry = function (cmd,arg) {
	if (isNaN(arg) && arg.indexOf("{") < 0)
		arg = '"'+arg+'"';
	
	var string = '{"'+cmd+'":'+arg+'}';
	this.entries.push(string);
}


Journal.prototype.toString = function () {	
	var string = "[";
	for (var i=0; i < this.entries.length; i++)
	{
		string += this.entries[i];
		if (i < this.entries.length-1)
			string += ",";
	}
	string += "]";
	return string;
}

// selection.class.js
function Selection () {
	this.id;
	this.uidListe = new Array();
}

function Selection (id) {
	this.id = id;
	this.uidListe = new Array();
}

Selection.prototype.addUID = function (uid) {
	if (uid.indexOf("_") != -1)
	{
		var tmpArr = uid.split("_");
		uid = tmpArr[1];
	}
	this.uidListe.push(uid);
}

Selection.prototype.searchUID = function (uid) {
	for (var i=0; i < this.uidListe.length ; i++ )
		if (this.uidListe[i] == uid)
			return i;

	return null;
}

Selection.prototype.del = function () {
	this.uidListe = new Array();
}

Selection.prototype.del = function (uid) {
	this.uidListe.splice(this.searchUID(uid), 1);
}

Selection.prototype.toString = function () {
	var string = "{'id':'"+this.id+"','UIDlist':[";
	for (var i=0; i<this.uidListe.length ; i++ )
	{
		string += "'"+this.uidListe[i]+"'";
		if (i < this.uidListe.length-1)
			string += ",";
	}
	string += "]}";
	return string;
}

// selectionMgt.js
var listStore = new Array();
var now = new Date();

function addSelection ()
{
	theJSON.newItem({
		uid: "list"+listStore.length,
		type: "auswahl",
		title: "Auswahl"+listStore.length
	});
	listStore.push(new Selection("Auswahl"+listStore.length));
	return "Auswahl"+(listStore.length-1);
}

function delSelection (itemID)
{
	var tmpTitle;
	var uid;
	var parentTitle;
	theJSON.fetchItemByIdentity({
		identity : itemID,
		onItem : function(item,request) {
			tmpTitle = theJSON.getValue(item,"title");
			var arr = itemID.split("topic_");
			if(arr.length > 1) {
				uid = itemID.split("topic_")[arr.length-1];
				parentTitle = itemID.split("topic_")[0];
			}
		}
	});
	
	if(parentTitle) {	// Topic loeschen
		theJSON.fetchItemByIdentity({
			identity: itemID,
			onItem : function (item, request) {
				theJSON.deleteItem(item);
				theJSON._pending={_newItems:{},_modifiedItems:{},_deletedItems:{}};
			}
		});
		delSelectionItem (uid, parentTitle);
		return;
	}
	
	if (confirm ("Soll die Auswahl "+tmpTitle+" wirklich unwiederbringlich entfernt werden?"))
	{
		theJSON.fetchItemByIdentity({
			identity: itemID,
			onItem : function (item, request) {
				theJSON.deleteItem(item);
			}
		});
		delete listStore[getListindexById(tmpTitle)];
		
		journal.addEntry('del',tmpTitle);
	}
}

function delSelectionItem (uid, tmpTitle) {
	listStore[getListindexById(tmpTitle)].del(uid);
}

function addSelectionFromFile(obj)
{
	if (typeof(obj.uid) == "string")
	{
		listStore.push(new Selection(obj.title));
		var parentItem = theJSON.newItem({
			uid: now.getTime()+"#"+obj.uid,
			type: "auswahl",
			title: obj.title 
		});
		_addSelectionFromFile(obj, parentItem);
	}
	else
		console.log("addSelectionFromFile - obj without uid");
}

function _addSelectionFromFile (obj, parentitem)
{
	listStore[listStore.length-1].addUID("101");
	obj.children.forEach(function (x) {
		if(x.uid == "101")
			return true;
		listStore[listStore.length-1].addUID(x.uid);
		
		theJSON.newItem ({
			uid:now.getTime()+"#"+x.uid,
			type:"auswahl",
			title:x.title
		},{parent:parentitem,attribute:"children"});
	});
	
	return true;
}

function getListindexById (needle)
{
	for (var i=0; i < listStore.length; i++)
		if (listStore[i] != undefined && listStore[i].id == needle)
			return i;
	return null;
}

function renameSelection (itemID)
{
	theJSON.fetchItemByIdentity({
		identity: itemID,
		onItem: function(item,request) {
		
			var newName = prompt("Bitte geben Sie den Namen ein...");
			var oldName = listStore[getListindexById(theJSON.getValue(item,"title"))].id;
			journal.addEntry('rn',oldName+'->'+newName);
			listStore[getListindexById(theJSON.getValue(item,"title"))].id = newName;
			if (newName != "" && newName != null)
				theJSON.setValue(item,"title",newName);
			
		}
	});
}

function saveSelection (itemID, type)
{
	var tmpTitle;
	if(isSelectionItem(itemID)){
		tmpTitle = getSelectionTitleFromItem(itemID);
	} else {
		theJSON.fetchItemByIdentity({
			identity: itemID,
			onItem: function(item, request) {
				tmpTitle = theJSON.getValue(item,'title');
			}
		});
	}
	var popupWindow = window.open('', "Download", "width=400,height=300,scrollbars=no,resizable=no");
	popupWindow.document.write('<meta http-equiv="refresh" content="0;URL=contentGenerator.php?type='+type+'&selection='+getSelectionUidListByTitle(tmpTitle)+'"><p>Ihr Download startet in K&uuml;rze!<br>Falls nicht, k&ouml;nnen Sie auch diesen <a href="contentGenerator.php?type='+type+'&selection='+getSelectionUidListByTitle(tmpTitle)+'">Link</a> ben&uuml;tzen.</p>');
	popupWindow.focus();
}

function addUIDtoSelection (selectionID, nodeID)
{
	if (nodeID.indexOf("_") != -1)
	{
		var tmpArr = nodeID.split("_");
		var uid = tmpArr[1];
	}
	listStore[getListindexById(selectionID)].addUID(nodeID);
	var tmpTitle;
	theJSON.fetchItemByIdentity({
		identity : uid,
		onItem : function(item,request) {
			tmpTitle = theJSON.getValue(item,"title");
		}
	});
	theJSON.fetch({
		query: {"title":selectionID},
		queryOptions: {deep:true}, 
		onItem: function (item, request) {
			var tmpItem = item;
			var newItem = theJSON.newItem({
				uid: selectionID+nodeID,
				type: "auswahl",
				title: tmpTitle
			}, {parent:item,attribute:"children"});
			
	journal.addEntry("changed", selectionID);

		}
	});
}

function isSelectionItem (uid) {
	var arr = uid.split("topic_");
	if(arr.length > 1)
		return true;
	return false;
}

function getSelectionTitleFromItem (uid) {
	var arr = uid.split("topic_");
	return arr[0];
}

function getSelectionUidListByIdTitle (uid, title)
{
	if(listStore[getListindexById(title)])
		return getSelectionUidListByTitle(title);

	var arr = uid.split("topic_");
	parentTitle = arr[0];

	return getSelectionUidListByTitle(parentTitle);
}

function getSelectionUidListByTitle (title)
{
	return listStore[getListindexById(title)].toString();
}

function selectionToChecklist(id)
{
	(function () {
		var itemStr = "";
		var title = "";
		if(isSelectionItem(id)){
			title = getSelectionTitleFromItem(id);
		} else {
			theJSON.fetchItemByIdentity({
				identity: id,
				onItem: function(item,request) {
					title = theJSON.getValue(item,"title");
				}
			});
		}
		itemStr = getSelectionUidListByTitle(title);
		var tmpTab = new dijit.layout.ContentPane({
			title: title+": Checkliste", 
			refreshOnShow:false, 
			preventCache:true, 
			closable:true, 
			href:getURL("contentGenerator.php?type=checklist&selection="+itemStr)});
		tmpTab.innerHTML = title + tmpTab.innerHTML;
		lesebereich.addChild(tmpTab);
		lesebereich.selectChild(tmpTab);
	})()
}
/*!
* AerWebCopy Engine [version 6.3.0]
* Copyright Aeroson Systems & Co.
* File mirrored from https://www.sicherheitshandbuch.gv.at/js/functions.js
* At UTC time: 2021-03-19 13:40:43.263588
*/
