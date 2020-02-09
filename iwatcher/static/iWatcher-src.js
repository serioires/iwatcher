//lat,lng -координаты, dev задается в виде количества 5-градусных секторов
var cams = [];
var cSelected; //выделенная пользователем
var newbounds;
var oldbounds;

function drawCamera(lat, lng, dev, id) {
  	if (!cams.find(item => item.id == id)) {
        let type = (dev == 80) ? 'fish':'cctv';
        let angle = (dev == 80) ? 0 : dev*5;

        let imgname = 'static/images/'+type+'.png';
    	let camImg = L.icon({
    		iconUrl: imgname,
      	  	iconSize: [16, 16],
      	  	iconAnchor: [8, 8]
    	});
        cams.push(L.marker([lat, lng], {
            icon: camImg,
            opacity:1,
            rotationAngle: angle
        }));
        cams[cams.length-1].id = id;
        cams[cams.length-1].dev = dev;
        if (!editor) {
            cams[cams.length-1].on ('click', function(ev) {
                if (cSelected != undefined) {
                    let type = (cSelected.dev == 80) ? 'fish':'cctv';
                    let clean = 'static/images/'+type+'.png';
                    let no_shadow = L.icon({iconUrl: clean,
                        iconSize: [16, 16],
                        iconAnchor: [8, 8]});
                    cSelected.setIcon(no_shadow);
                }
                cSelected = ev.target;
                rInfo(cSelected.id);
                let type = (cSelected.dev == 80) ? 'fish':'cctv';
                let imnm = 'static/images/'+type+'.png';
                let sImg = L.icon({
                    iconUrl: imnm,
                    iconSize: [16, 16],
                    iconAnchor: [8, 8],
                    shadowUrl: 'static/images/select.png',
                    shadowSize: [32, 32],
                    shadowAnchor: [16, 16]});
                cSelected.setIcon(sImg);
                document.getElementById("lat").innerHTML = cSelected.getLatLng().lat.toFixed(6);
                document.getElementById("lon").innerHTML = cSelected.getLatLng().lng.toFixed(6);;
            });
        }
        markers.addLayer(cams[cams.length-1]);
  	}
}


// функции с именами r[Somename] дергают за точки входа /api/[somename]
function rInfo(id) {
	fetch(`api/info/${id}`, {method: 'POST'})
  	  	.then(response => response.json())
        .then( info => {
            if (cSelected.id == info.id) {
                document.getElementById("rating").innerHTML = info.rating;
                document.getElementById("about").innerHTML = info.about;
                document.getElementById("added").innerHTML = info.added;
            }
        })
  	  	.catch(error => alert(error.message))
}


function rRate(id) {
	fetch(`api/rate/${id}`, {method: 'POST'})
  	  	.then(response => response.json())
        .then(data => data.forEach(
            upd => {
                if (cSelected.id == upd.id) {
                    document.getElementById("rating").innerHTML = upd.rating;
                }
            }
        ))
  	  	.catch(error => alert(error.message));
}


function rGet() {
  	let requests = prepRanges().map(range => fetch('api/get', {
  	  	method: 'POST',
  	  	headers: {
  	  	  	'Content-Type': 'application/json;charset=utf-8'
  	  	},
  	  	body: JSON.stringify(range)
  	})
    .then(response => response.json()));
  	Promise.all(requests)
  	  	.then(responses => responses.forEach(
            data => data.forEach(
                camera => drawCamera(camera.lat, camera.lon, camera.dev, camera.id)
            )
        ))
  	  	.catch(error => alert(error.message));

}


function rAdd(){
	if (newcamera){
	    let latlng = newcamera.getLatLng();
        let dev = (document.getElementById('fish').checked) ? 80 : document.getElementById("dev").value;
	    addthis = {
	         lat: latlng.lat.toFixed(6),
			 lon: latlng.lng.toFixed(6),
			 dev: dev,
			 about: document.getElementById("new_about").value
	    }
        fetch('api/add', {
            method: 'POST',
            headers: {
      	  	  	'Content-Type': 'application/json;charset=utf-8'
      	  	},
      	  	body: JSON.stringify(addthis)
        })
        .then(response => response.json())
        .then(data => data.forEach(
            camera => {
                newcamera.remove();
                newcamera = undefined;
                drawCamera(camera.lat, camera.lon, camera.dev, camera.id);
            }
        ))
	}
}


// Утилиты
function prepRanges() {
  	let ranges = [];
  	if (!oldbounds.contains(newbounds)) {

  	  	if (newbounds.overlaps(oldbounds)) {
  	  	  	if (newbounds.getWest().toFixed(6) < oldbounds.getWest().toFixed(6)) {
  	  	  	  	ranges.push({
  	  	  	  	  	w: newbounds.getWest().toFixed(6),
  	  	  	  	  	e: oldbounds.getWest().toFixed(6),
  	  	  	  	  	n: newbounds.getNorth().toFixed(6),
  	  	  	  	  	s: newbounds.getSouth().toFixed(6)
  	  	  	  	});
  	  	  	}
  	  	  	if (newbounds.getEast().toFixed(6) > oldbounds.getEast().toFixed(6)) {
  	  	  	  	ranges.push({
  	  	  	  	  	w: oldbounds.getEast().toFixed(6),
  	  	  	  	  	e: newbounds.getEast().toFixed(6),
  	  	  	  	  	n: newbounds.getNorth().toFixed(6),
  	  	  	  	  	s: newbounds.getSouth().toFixed(6)
  	  	  	  	});
  	  	  	}
  	  	  	if (newbounds.getNorth().toFixed(6) > oldbounds.getNorth().toFixed(6)) {
  	  	  	  	ranges.push({
  	  	  	  	  	w: newbounds.getWest().toFixed(6),
  	  	  	  	  	e: newbounds.getEast().toFixed(6),
  	  	  	  	  	n: newbounds.getNorth().toFixed(6),
  	  	  	  	  	s: oldbounds.getNorth().toFixed(6)
  	  	  	  	});
  	  	  	}
  	  	  	if (newbounds.getSouth().toFixed(6) < oldbounds.getSouth().toFixed(6)) {
  	  	  	  	ranges.push({
  	  	  	  	  	w: newbounds.getWest().toFixed(6),
  	  	  	  	  	e: newbounds.getEast().toFixed(6),
  	  	  	  	  	n: oldbounds.getSouth().toFixed(6),
  	  	  	  	  	s: newbounds.getSouth().toFixed(6)
  	  	  	  	});
  	  	  	}

  	  	} else {
  	  	  	ranges.push({
  	  	  	  	w: newbounds.getWest().toFixed(6),
  	  	  	  	e: newbounds.getEast().toFixed(6),
  	  	  	  	n: newbounds.getNorth().toFixed(6),
  	  	  	  	s: newbounds.getSouth().toFixed(6)
  	  	  	});
  	  	}
  	} else if (newbounds === oldbounds) {
  	  	ranges.push({
  	  	  	w: newbounds.getWest().toFixed(6),
  	  	  	e: newbounds.getEast().toFixed(6),
  	  	  	n: newbounds.getNorth().toFixed(6),
  	  	  	s: newbounds.getSouth().toFixed(6)
  	  	});
  	}
  	return ranges;
}


function setCType() {
    let type = ((document.getElementById('fish').checked)? 'fish' : 'cctv');
    if (newcamera) {
        let imgname = 'static/images/'+type+'.png';
		let camImg = L.icon({
            iconUrl: imgname,
            iconSize: [16, 16],
            iconAnchor: [8, 8]});
        newcamera.setIcon(camImg);
    }
    if (type == 'fish') {
        document.getElementById('dev').setAttribute('disabled',"disabled");
    } else {
        document.getElementById('dev').removeAttribute('disabled');
    }
}


function oldCamRemove() {
	if (cams.length) {
		for (let i = (cams.length - 1); i > -1; i--) {
			lalg = cams[i].getLatLng();
			if (!(newbounds.contains(lalg))) {
                markers.removeLayer(cams[i]);
				cams[i].remove();//удаляет маркер
				cams.splice(i, 1);//убирает освободившийся элемент
			}
		}
	}
}


// Обработчики событий
function onMapUpd() {
	if (map.getZoom() > 8) {
		newbounds = map.getBounds();
		oldCamRemove();

		rGet();
		oldbounds = newbounds;
	}
	setCookie("lat", (map.getCenter()).lat.toFixed(6));
	setCookie("lon", (map.getCenter()).lng.toFixed(6));
}


function onMapLoad() {
	oldbounds = map.getBounds();
	newbounds = oldbounds;
	rGet(oldbounds);
}
