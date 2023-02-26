  $(document).ready(function() {

    var centerMap = SMap.Coords.fromWGS84(14.40, 50.08);
    var m = new SMap(JAK.gel("m"));
    m.addControl(new SMap.Control.Sync());
    var l = m.addDefaultLayer(SMap.DEF_TURIST).enable();
    m.addDefaultControls();
    var mouse = new SMap.Control.Mouse(SMap.MOUSE_PAN | SMap.MOUSE_WHEEL | SMap.MOUSE_ZOOM); /* Ovládání myší */
    m.addControl(mouse);

    var layer = new SMap.Layer.Marker();
    m.addLayer(layer);
    layer.enable();

    var vrstva = new SMap.Layer.Geometry();
    m.addLayer(vrstva).enable();

    var znacka1, znacka2;
    var data = [];
    var souradnice = [SMap.Coords.fromWGS84(18.7858278, 48.6465275),SMap.Coords.fromWGS84(11.8095094, 51.1302525)];
    var znacky = [];

    var cz = m.computeCenterZoom(souradnice); /* Spočítat pozici mapy tak, aby značky byly vidět */
    m.setCenterZoom(cz[0], cz[1]);

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
              anchor: {left:10, bottom: 1}  /* Ukotvení značky za bod uprostřed dole */
          }
        var znacka = new SMap.Marker(coords, null, options);
        znacka.decorate(SMap.Marker.Feature.Draggable);
        layer.addMarker(znacka);
        znacky.splice(znacky.length-1,0,znacka);
        spocti();
      }
    }

    function remove_marker(e, elm) {
      if ((e.target != znacka1) && (e.target != znacka2)) {
        layer.removeMarker(e.target);
        const index = znacky.indexOf(e.target);
        znacky.splice(index,1);
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
              anchor: {left:10, bottom: 1}  /* Ukotvení značky za bod uprostřed dole */
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
              anchor: {left:10, bottom: 1}  /* Ukotvení značky za bod uprostřed dole */
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

    const nalezeno_route = (od, do_, route) => {
      const od_id = od.getId()
      const do_id = do_.getId()

      var coords = route.getResults().geometry;
      var g = new SMap.Geometry(SMap.GEOMETRY_POLYLINE, null, coords);
      vrstva.addGeometry(g);

      koef = (3000<=od_id<=3999) && (3000<=do_id<=3999) ? 2/3 : 3/4;
      cas = Math.round(route.getResults().time/60*koef);
      cas = od_id<3000 ? cas+5 : cas;
      delka = Math.round(route.getResults().length/100)/10;
      data.push({'od':od_id,'do':do_id,'gps_od':od.getCoords(),'gps_do':do_.getCoords(),'cas':cas,'delka':delka});
      $("#vysledek").append('Od: '+od_id+' Do: '+do_id+'<br>');
      $("#vysledek").append('Čas: '+cas+' Délka: '+delka+'<br>');
    }

function spocti() {
    vrstva.removeAll();
    $("#vysledek").empty();
    route_coords = znacky.map(znacka => znacka.getCoords());
    data = []

    SMap.Route.route(route_coords, {criterion:"turist1", geometry: true})
              .then(route => nalezeno_route(znacka1,znacka2,route));
    SMap.Route.route(route_coords.slice().reverse(), {criterion:"turist1", geometry: true})
              .then(route => nalezeno_route(znacka2,znacka1,route));
}

$("#zapis").click(function(){
  if (Object.keys(vrstva.getGeometries()).length) {
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
