# Instalacion de Recursos

> [!NOTE]
> Distribucion: Debian 12 (Bookworm)

## Python3.10

> Voy a usar conda para crear un entorno virtual de python3.10, la instalacion de conda esta en el repositorio de SAD

```bash
conda create -n sw python=3.10
```

> Para activar el entorno virtual

```bash
conda activate sw
```

> Para instalar "Selenium" en el entorno virtual

```bash
pip install selenium
```

> Para desactivar el entorno virtual

```bash
conda deactivate
```

## PyCharm

> Voy a usar VSCode, no me gusta PyCharm

> [!CAUTION]
> Porfavor, no uses VSCode con snap o flatpak, instalalo a traves de apt o dpkg

```bash
curl -fSsL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor | sudo tee /usr/share/keyrings/vscode.gpg >/dev/null
echo deb [arch=amd64 signed-by=/usr/share/keyrings/vscode.gpg] https://packages.microsoft.com/repos/vscode stable main | sudo tee /etc/apt/sources.list.d/vscode.list
sudo apt update
sudo apt install code
```

### BurpSuite

```bash
wget https://portswigger.net/burp/releases/community/latest

sudo chmod +x burpsuite_community_linux_v2023_11_1_5.sh

./burpsuite_community_linux_v2023_11_1_5.sh
```

## Wireshark

```bash
sudo apt install wireshark
```

## Geckodrive

> En Debian parece que viene instalado por defecto

```bash
python pruebaGeckodrive.py
```

## View Source Chart

> Crear un marcador de favoritos con un nombre y este script como URL

```javascript
javascript:wprops='';function getComments(pnode) {function doGetComments(node) {if (node.nodeType == 8) {node.nodeValue=node.nodeValue.replace(/</g,"<vsc");} else if (node.childNodes != null) {for (var i=0;i < node.childNodes.length;++i) {doGetComments(node.childNodes.item(i));}}return node;}return doGetComments(pnode);}function vsc_getScripts(scriptTagArray){scrTags=scriptTagArray;for(var si=0; si<scrTags.length; si++) {if (scrTags[si].childNodes) {if(scrTags[si].childNodes.length > 1){var thisisthelength = scrTags[si].childNodes.length;for(var xx=1; xx<thisisthelength;xx++){scrTags[si].childNodes[xx].nodeValue="";}}s=scrTags[si].text;s=s.replace(/;/gi,'vsc;');s=s.replace(/</gi,'&lt;vsc ');s=s.replace(/>/gi,'&gt;vsc');s=s.replace(/{/gi,'{vsc');scrTags[si].text=s;}}return scrTags;}function VSCb(){vrs_doctypeTag="";for(var len=0; len<document.childNodes.length; len++){rootElm=document.childNodes[len];if(rootElm.nodeType==1){if(rootElm.attributes.length>0){htatts = "";for(at=0; at<rootElm.attributes.length; at++){htatts += " " + rootElm.attributes[at].nodeName + "=\"" + rootElm.attributes[at].nodeValue + "\"";}vrs_htmlTag="&lt;html <span style=\"color:#669966;\">"%20+%20htatts%20+%20"</span>&gt;";}else{vrs_htmlTag="&lt;html&gt;";}}else{var%20doc_type%20=%20document.doctype;vrs_doctypeTag%20=%20"<span%20style=\"color:#37A8E9;font-style:%20italic;\">&lt;!DOCTYPE%20"+doc_type.name;vrs_doctypeTag%20+=%20(doc_type.publicId)%20?%20"%20PUBLIC%20\""+doc_type.publicId+"\""%20:%20"";/*%20SYSTEM*/vrs_doctypeTag%20+=%20(doc_type.systemId)%20?%20"<br>\""+%20doc_type.systemId+"\"&gt;"%20:%20"&gt;";vrs_doctypeTag%20+=%20"</span><BR>";}}dom=document.documentElement.cloneNode(true);vsc_getScripts(dom.getElementsByTagName("script"));getComments(dom);moString%20=%20'onmouseout=\"this.style.boxShadow=\'\'\;\"%20onmouseover="this.title=this.childNodes[0]%20&&%20this.childNodes[0].nodeType!=1%20?%20this.childNodes[0].nodeValue%20:%20this.title;this.style.cursor=';var%20vscContainer_TitleCursor%20=%20moString+'\'pointer\'\;this.style.cursor==\'pointer\'%20?%20this.style.boxShadow=\'0%200%20.75em%20#CCF\'\%20:%20this.style=this.style;"';var%20vscTag_TitleCursor=moString+'\'auto\'\;"';elms=dom.innerHTML;elms=elms.replace(/&/g,'&amp;');elms=elms.replace(/</g,'&lt;');elms=elms.replace(/>/g,'&gt;');%20elms=elms.replace(/(&lt;(?!%20?\/)(?=head(?=%20|&)|title|body|script|style|article|section|header|aside|footer|nav|dialog|figure|canvas|svg|div|span|p(?=%20|&)|table|thead|tfoot|tr|th|td|frameset|iframe|ul|ol|dl|dt|dd|li(?=%20|&)|blockquote))(\w+)/gi,'<div%20id="$2Tag"'+vscContainer_TitleCursor+'>$1$2');elms=elms.replace(/(&lt;(?!%20?\/)(?=a(?=%20|&)|form|select|option|legend|fieldset|textarea|h[1-6]|center|caption|code|em(?=%20|&)|i(?=%20|&)|strong|b(?=%20|&)|font|m(?=%20|&)|progress|time|meter))(\w+)/gi,'<div%20id="$2Tag"'+vscTag_TitleCursor+'>$1$2');%20elms=elms.replace(/(&lt;%20?\/(head|title|body|script|style|article|section|header|aside|footer|nav|dialog|figure|canvas|svg|div|span|table|thead|tfoot|tr|th|td|frameset|iframe|ul|ol|dl|dt|dd|li|p|blockquote|code|a|form|select|option|legend|fieldset|textarea|em|i|strong|b|font|h[1-6]|center|caption|m|time|progress|meter)&gt;)/gi,'$1</div>');elms=elms.replace(/&lt;!--/gi,'<div%20id="commTag"'+vscContainer_TitleCursor+'>&lt;!--');elms=elms.replace(/--&gt;/gi,'--&gt;</div>');elms=elms.replace(/&lt;/g,'<br>&lt;');elms=elms.replace(/&gt;/g,'&gt;<br>');elms=elms.replace(/>\s*<br>/g,'>');elms=elms.replace(/}(?!&lt;\/)/g,'}<br>');elms=elms.replace(/{vsc/g,'{<br>');elms=elms.replace(/&lt;vsc/g,'&lt;');elms=elms.replace(/&amp;lt;vsc%20/gi,'&lt;');elms=elms.replace(/&amp;gt;vsc/gi,'&gt;');elms=elms.replace(/vsc;/gi,';<br>');elms=elms.replace(/<br>(\s*)<br>/gi,'<br>');w=window.open('','',wprops);arsc=w.document.createElement('script');w.document.getElementsByTagName('head')[0].appendChild(arsc);arsc.innerHTML="window.addEventListener(\"mouseup\",vrsc_getTarget,false);var%20collCon=new%20Array();function%20vrsc_getTarget(e){if(window.getSelection()==''){if(document.title.indexOf('View%20Source%20Chart')%20!=%20-1){var%20is_vrsClick%20=%20(e.type.toLowerCase()%20==%20'mouseup'%20&&%20e.button%20!=%202)%20?%20true%20:%20false;var%20containerV=e.target;var%20thisVSCBorder=(containerV.style.cursor=='pointer'%20?%20true%20:%20false);if(is_vrsClick%20&&%20thisVSCBorder){if(containerV.childNodes[0].nodeType%20!=%201){collCon.push(containerV.innerHTML);containerV.innerHTML='<'+'input%20type=hidden%20value='+(collCon.length-1)+'>';var%20VSC_newTop=VSC_getPos(containerV);if((VSC_newTop.top<document.body.scrollTop)%20||%20(VSC_newTop.top%20>%20(document.body.scrollTop+window.clientHeight))){document.body.scrollTop=VSC_newTop.top-e.clientY;}}else{var%20hiddenValue%20=%20parseInt(containerV.childNodes[0].value);containerV.innerHTML%20=%20collCon[hiddenValue];collCon[hiddenValue]%20=%20'';if(window.getSelection){window.getSelection().removeAllRanges();}else{document.selection.clear()}}}}}}function%20VSC_getPos(VSC_obj){var%20VSC_output%20=%20new%20Object();var%20VSC_mytop=0,%20VSC_myleft=0;while(VSC_obj){VSC_mytop+=%20VSC_obj.offsetTop;VSC_myleft+=%20VSC_obj.offsetLeft;VSC_obj=%20VSC_obj.offsetParent;}VSC_output.left%20=%20VSC_myleft;VSC_output.top%20=%20VSC_mytop;return%20VSC_output;}";st=document.createElement('style');w.document.getElementsByTagName('head')[0].appendChild(st);st.innerHTML='div{padding:5px;margin:7px;font-family:verdana;font-size:10px;word-wrap:break-word;}#headTag{border:dashed%201px%20#dcdcdc;}#titleTag{color:#556b2f;font-weight:bold;border:dashed%201px%20#556b2f;}#scriptTag{color:#009900;border:dashed%201px%20#009900;}#statements{border:1px%20dashed;}#styleTag{color:#8b008b;border:dashed%201px%20#8b008b;background-color:#ffffff;%20}#rulesChar{%20margin:0px%203px%200px%207px;}#bodyTag,#canvasTag,#svgTag{border:dashed%201px%20#000000;}#divTag{background-color:#e6e6fa;border:solid%201px%20#d8bfd8;}#spanTag{background-color:#ffffe0;border:solid%201px%20#FFDF80;}#tableTag,#articleTag,#headerTag,#sectionTag,#asideTag,#footerTag,#navTag,#figureTag{background-color:#E8F0FF;margin:9px;border:solid%201px%20#99ccff;}#tbodyTag,#theadTag,#tfootTag{margin:4px}#trTag{border:dashed%201px%20#99ccff;background-color:#E8F0FF;}#thTag,#tdTag,#figcaptionTag{background-color:#E8F0FF;border:dotted%201px%20#99ccff;}#framesetTag{margin:7px;background-color:#ffe4ca;border:solid%201px%20#deb887;}#iframeTag{background-color:#c2e0ec;border:solid%201px%20#94c8de;}#ulTag,#olTag,#dialogTag,#dlTag{background-color:#E6F7DA;border:solid%201px%20#ADCA98;}#liTag,#dtTag{background-color:#E6F7DA;border:dotted%201px%20#ADCA98;}#ddTag{background-color:#E6F7DA;margin:7px%2027px%207px%2027px;border:dashed%201px%20#ADCA98;}#pTag{background-color:#fce0de;border:solid%201px%20#f9c3bf;}#blockquoteTag{background-color:#FBF0E9;border:solid%201px%20#F3D9C7;}#commTag{color:#999999;border:%20dashed%201px%20#999999;}#aTag{color:#000099;margin:0px%203px%200px%207px;}#emTag,#iTag,#strongTag,#bTag,#uTag,#h1Tag,#h2Tag,#h3Tag,#h4Tag,#h5Tag,#h6Tag,img,#centerTag,#fontTag,#formTag,#selectTag,#fieldsetTag,#legendTag,#textareaTag{margin:0px%203px%200px%207px;}#emTag,#iTag{font-style:italic;}#strongTag,#bTag{font-weight:bold;}#uTag{text-decoration:underline;}#h1Tag,#h2Tag,#h3Tag,#h4Tag,#h5Tag,#h6Tag{font-weight:bold;}';w.document.body.innerHTML='<span%20style=\"font-family:verdana;font-size:10px;\">'+vrs_doctypeTag+vrs_htmlTag+elms+'&lt;/html&gt</span>';w.document.title='View%20Source%20Chart%20bookmarklet';}VSCb();
```