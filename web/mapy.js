  $(document).ready(function() {

    var centerMap = SMap.Coords.fromWGS84(14.40, 50.08);
    var m = new SMap(JAK.gel("m"));
    m.addControl(new SMap.Control.Sync());
    var l = m.addDefaultLayer(SMap.DEF_TURIST).enable();
    m.addDefaultControls();
    var mouse = new SMap.Control.Mouse(SMap.MOUSE_PAN | SMap.MOUSE_WHEEL | SMap.MOUSE_ZOOM); /* Ovládání myší */
    m.addControl(mouse);

//    var poiLayer = new SMap.Layer.Marker(undefined, {
//        poiTooltip: true
//    });
//    m.addLayer(poiLayer).enable();
//
//    var dataProvider = m.createDefaultDataProvider();
//    dataProvider.setOwner(m);
//    dataProvider.addLayer(poiLayer);
//    dataProvider.setMapSet(SMap.MAPSET_BASE);
//    dataProvider.enable();

    var layer = new SMap.Layer.Marker();
    m.addLayer(layer);
    layer.enable();

    var vrstva = new SMap.Layer.Geometry();
    m.addLayer(vrstva).enable();

    var znacka1, znacka2;
    var souradnice = [SMap.Coords.fromWGS84(18.7858278, 48.6465275),SMap.Coords.fromWGS84(11.8095094, 51.1302525)];
    var znacky = [];

    var cz = m.computeCenterZoom(souradnice); /* Spočítat pozici mapy tak, aby značky byly vidět */
    m.setCenterZoom(cz[0], cz[1]);

    function createURL(txt) {
        var znacka = JAK.mel("div");
        var obrazek = JAK.mel("img", {src:SMap.CONFIG.img+"/marker/drop-red.png"});
        znacka.appendChild(obrazek);

        var popisek = JAK.mel("div", {}, {position:"absolute", left:"0px", top:"2px", textAlign:"center", width:"22px", color:"white", fontWeight:"bold"});
        popisek.innerHTML = txt;
        znacka.appendChild(popisek);
        return znacka
    }

    function start(e) { /* Začátek tažení */
        var node = e.target.getContainer();
        node[SMap.LAYER_MARKER].style.cursor = "help";
    }

    function stop(e) {
        var node = e.target.getContainer();
        node[SMap.LAYER_MARKER].style.cursor = "";
        vrstva.removeAll();
        spocti();
    }

    function click(e, elm) {
      if (Object.keys(vrstva.getGeometries()).length) {
        var coords = SMap.Coords.fromEvent(e.data.event, m);
          var options = {
              title: `průchozí bod {znacky.length-1}`,
              anchor: {left:10, bottom: 1},  /* Ukotvení značky za bod uprostřed dole */
              url: createURL(znacky.length-1)
          }
        var znacka = new SMap.Marker(coords, null, options);
        znacka.decorate(SMap.Marker.Feature.Draggable);
        layer.addMarker(znacka);
        znacky.splice(znacky.length-1,0,znacka);
        spocti();
      }
    }

    function isPruchozi(znacka) {
      return znacka.getTitle().startsWith('průchozí bod');
    }

    function remove_marker(e, elm) {
      if (isPruchozi(e.target)) {
        const index = znacky.indexOf(e.target);
        for (let i = index; i < znacky.length-2; i++) {
          znacky[i].setCoords(znacky[i+1].getCoords())
        }
        layer.removeMarker(znacky[znacky.length-2]);
        znacky.splice(znacky.length-2,1);
        spocti();
      }
    }

    var signals = m.getSignals();
    signals.addListener(window, "marker-drag-stop", stop);
    signals.addListener(window, "marker-drag-start", start);
    signals.addListener(window, "map-click", click);
    signals.addListener(window, "marker-click", remove_marker);

  $(".selectpicker").selectpicker();

$(document).on('keyup', '.filter-component .bs-searchbox input', function (e) {
    let searchData = e.target.value;
    let mySelect = e.target.parentElement.parentElement.parentElement.firstChild;

    eel.chplist(searchData)(newOptions => $(mySelect).empty().append(newOptions).selectpicker('refresh').selectpicker('render'));
});

    function splitFirstWord(str) {
        let spaceIndex = str.indexOf(' ');
        return spaceIndex === -1 ? [str,''] : [str.substring(0, spaceIndex),str.substring(spaceIndex+1)];
    }

    function removeFirstWord(str) {
        let spaceIndex = str.indexOf(' ');
        return spaceIndex === -1 ? '' : str.substring(spaceIndex+1);
    }

$("#od").on('hide.bs.select', function () {
    const coords_found = function (result) {
        if (result) {
          var c = SMap.Coords.fromWGS84(result.x,result.y); /* Souřadnice značky, z textového formátu souřadnic */

          var options = {
              title:removeFirstWord($("#od  option:selected").text()),
              anchor: {left:10, bottom: 1},  /* Ukotvení značky za bod uprostřed dole */
              url: createURL("A")
          }

          if ($("#od  option:selected").val() != $("#do  option:selected").val()) {
              znacka1 = new SMap.Marker(c, $("#od  option:selected").val(), options);
              znacka1.decorate(SMap.Marker.Feature.Draggable);
              layer.addMarker(znacka1);
          } else {
              znacka1 = znacka2;
          }
          if (znacky.length > 1) {
            znacky.splice(0,znacky.length-1,znacka1);
          } else {
            znacky.unshift(znacka1);
          }
          souradnice = znacky.map(znacka => znacka.getCoords());
          if (znacky.length > 1) {spocti();}
        }


        var cz = m.computeCenterZoom(souradnice); /* Spočítat pozici mapy tak, aby značky byly vidět */
        m.setCenterZoom(cz[0], cz[1]);
    }

    vrstva.removeAll();
    znacky.forEach(znacka => {
      if (znacka != znacka2) {
        layer.removeMarker(znacka);
      }
    });
    eel.coords($("#od").val())(coords_found);
});

$("#do").on('hide.bs.select', function () {
    const coords_found = function (result) {
        if (result) {
          var c = SMap.Coords.fromWGS84(result.x,result.y); /* Souřadnice značky, z textového formátu souřadnic */

          var options = {
              title:removeFirstWord($("#do  option:selected").text()),
              anchor: {left:10, bottom: 1},  /* Ukotvení značky za bod uprostřed dole */
              url: createURL("B")
          }

          if ($("#od  option:selected").val() != $("#do  option:selected").val()) {
              znacka2 = new SMap.Marker(c, $("#do  option:selected").val(), options);
              znacka2.decorate(SMap.Marker.Feature.Draggable);
              layer.addMarker(znacka2);
          } else {
              znacka2 = znacka1;
          }
          if (znacky.length > 1) {
            znacky.splice(1,znacky.length,znacka2);
          } else {
            znacky.push(znacka2);
          }
          souradnice = znacky.map(znacka => znacka.getCoords());
          if (znacky.length > 1) {spocti();}
        }


        var cz = m.computeCenterZoom(souradnice); /* Spočítat pozici mapy tak, aby značky byly vidět */
        m.setCenterZoom(cz[0], cz[1]);
    }

    vrstva.removeAll();
    znacky.forEach(znacka => {
      if (znacka != znacka1) {
        layer.removeMarker(znacka);
      }
    });
    eel.coords($("#do").val())(coords_found);
});

function isHorska(id) {
  return (id <= 3296) && (id >= 3261)
}

function isCheckpoint(id) {
  return (id <= 3999) && (id >= 3000)
}

    const nalezeno_route = (od, do_, elm_cas, elm_km, route) => {
      const od_id = od.getId()
      const do_id = do_.getId()

      var coords = route.getResults().geometry;
      var g = new SMap.Geometry(SMap.GEOMETRY_POLYLINE, null, coords);
      vrstva.addGeometry(g);
      delka = Math.round(route.getResults().length/100)/10;
      koef = (delka<=7) && (!isHorska(od_id)) && (!isHorska(do_id)) && ((!isCheckpoint(od_id)) || (!isCheckpoint(do_id))) ? 2/3 : 3/4;
      console.log(koef);
      cas = Math.round(route.getResults().time/60*koef);
      cas = od_id<3000 ? cas+5 : cas;
      elm_cas.val(cas);
      elm_km.val(delka);
      $(".trasa").show();
    }

function spocti() {
    vrstva.removeAll();

    $(".trasa").hide();
    $(".vysledek").val('');
    $("#vysledek").empty()
    route_coords = znacky.map(znacka => znacka.getCoords());

    SMap.Route.route(route_coords, {criterion:"turist1", geometry: true})
              .then(route => nalezeno_route(znacka1,znacka2,$('#cas_tam'),$('#km_tam'),route));
    SMap.Route.route(route_coords.slice().reverse(), {criterion:"turist1", geometry: true})
              .then(route => nalezeno_route(znacka2,znacka1,$('#cas_zpet'),$('#km_zpet'),route));
}

$("#zapis").click(function(){
  if (Object.keys(vrstva.getGeometries()).length) {
    $(".trasa").hide();
    const data = [{'od':znacka1.getId(),'do':znacka2.getId(),'gps_od':znacka1.getCoords(),'gps_do':znacka2.getCoords(),
                   'cas':$('#cas_tam').val(),'delka':$('#km_tam').val()},
                  {'od':znacka2.getId(),'do':znacka1.getId(),'gps_od':znacka2.getCoords(),'gps_do':znacka1.getCoords(),
                  'cas':$('#cas_zpet').val(),'delka':$('#km_zpet').val()}];
    eel.send_data(data)((result) => $("#vysledek").empty().append(result));
  }
});

eel.expose(list_coords)
function list_coords(items) {
            obj = {};
            var interval = 1000; // how much time should the delay between two iterations be (in milliseconds)?
            var promise = Promise.resolve();
            items.forEach(function (query) {
              promise = promise.then(function () {
                if (query.id<3000) {
                  query.nazev = query.nazev + ' vlaková stanice';
                }
                if (query.id>3999) {
                  query.nazev = query.nazev + ' zastávka tramvaje';
                }
                new SMap.Geocoder(query.nazev, geo => {
                    if (!geo.getResults()[0].results.length) {
                        obj[query.id] = {'x':0.0,'y':0.0};
                    } else {
                        obj[query.id] = geo.getResults()[0].results.shift().coords;
                    }
                });
                return new Promise(function (resolve) {
                  setTimeout(resolve, interval);
                });
              });
            });

            promise.then(function () {
              eel.send_coords(obj);
            });

}

function coords(id,nazev) {
  const nalezeno = (id,geo) => {
    if (!geo.getResults()[0].results.length)
      {eel.send_coords({'id':id,'x':0.0,'y':0.0});}
    else {
      const coords = geo.getResults()[0].results.shift().coords;
      eel.send_coords({'id':id,'x':coords.x,'y':coords.y});
    }
  }
}

});
