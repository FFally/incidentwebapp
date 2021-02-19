require(["dojo/_base/declare", "dojo/dom", "dojox/form/Uploader", "dijit/Dialog"], function(declare, dom){
	declare("js.myUploadDialog", dijit.Dialog, {
     createUI: function(){
          this.set("title", "Upload File");       
          this.set("content",
                     "<div >" +
                           "<table width='100%' border='0'  cellspacing='5' >" +
                                  "<tr>" +            
                                        "<td>Browse:</td>" +
                                        "<td><div data-dojo-type='dojox.form.Uploader'></div></td>" +
                                  "</tr>" +
                          "</table>"+                        
                     "</div>"
             );
          
           var uploadUrl = "contentGenerator.php?type=file";
           
           var uploader = new dojox.form.Uploader(
                   {
                      id:'fileUpload',
                      uploadUrl:uploadUrl, 
                      uploadOnChange:false, 
                      selectMultipleFiles:false
                   },
                   dom.byId('fileUploader')
          );
           
          uploader.startup(); 
     }
	});
});
/*!
* AerWebCopy Engine [version 6.3.0]
* Copyright Aeroson Systems & Co.
* File mirrored from https://www.sicherheitshandbuch.gv.at/js/myUploadDialog.js
* At UTC time: 2021-02-19 14:55:57.475061
*/
