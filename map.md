---
layout: page
title: MemExp on Map
description: Map showcasing the travelled places.
---

<html>
<head>
	<link rel="stylesheet" type="text/css" href="css/flags/flag-icon.min.css">
	<link rel="stylesheet" href="https://unpkg.com/leaflet@1.3.1/dist/leaflet.css"
	integrity="sha512-Rksm5RenBEKSKFjgI3a41vrjkw4EVPlJ3+OiI65vTjIdo9brlAacEuKOiQ5OFh7cOI1bkDwLqdLw3Zg0cRJAAQ=="
	crossorigin=""/>
	<script src="{{site.baseurl}}/js/country.js"></script>
	<script src="https://unpkg.com/leaflet@1.3.1/dist/leaflet.js"
	integrity="sha512-/Nsx9X4HebavoBvEBuyp3I7od5tA0UzAxs+j83KgC8PU0kgB4XiK4Lfe4y4cgBtaRJQEIFCW+oC506aPT2L1zw=="
	crossorigin=""></script>
	<style type="text/css">
		#mapid {
			height: 500px; 
			width: 100%;
		}
		.leaflet-container {
			background-color: #8BD1E3 !important
		}
		.two{
			width: 0% !important;
		}
		.eight{
			width: 92% !important;
		}
		@media (max-width: 550px){
			.eight{
				width: 100% !important;
			}
		}

	.tooltip-inner {
		padding: 0 5px;
		border-radius: 6px;
		font-family: Arial, Helvetica, sans-serif;
	  	background-color: #191919;
  		color: #FFFFFF;
  		font-size: 0.75em;
	}

	</style>
</head>
<body>
	<center>
		<!-- <h1 style="margin-top: 0px; font-size: 1.5em">8/29 Indian States. 0/7 Indian Union Territories.<br>7/193 Countries.<br>2/7 Continents.</h1> -->
		<span style="font-size: 1em;"><strong>Tip:</strong> You can see the respective photos of the MemExps by zooming in and <strong>cliking on the points</strong></span>
	</center>
	<div id="mapid" style="margin-top: 10px;"></div>
	<div id="countries" style="margin-top: 3%;">
		<center>
			<!-- https://github.com/lipis/flag-icon-css/tree/master/flags/4x3 -->
			<!-- https://www.nationsonline.org/oneworld/country_code_list.htm -->
			<span title="1.India" class="flag-icon flag-icon-in" data-toggle="tooltip"></span>
			<span title="2.Ireland" class="flag-icon flag-icon-ie" data-toggle="tooltip"></span>
			<span title="3.France" class="flag-icon flag-icon-fr" data-toggle="tooltip"></span>
			<span title="4.Belgium" class="flag-icon flag-icon-be" data-toggle="tooltip"></span>
			<span title="5.Netherlands" class="flag-icon flag-icon-nl" data-toggle="tooltip"></span>
			<span title="6.Monaco" class="flag-icon flag-icon-mc" data-toggle="tooltip"></span>
			<span title="7.Spain" class="flag-icon flag-icon-es" data-toggle="tooltip"></span>
			<span title="8.Thailand" class="flag-icon flag-icon-th" data-toggle="tooltip"></span>
			<span title="9.USA" class="flag-icon flag-icon-us" data-toggle="tooltip"></span>
		</center>
	</div>
	<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
	<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
	<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
	<script type="text/javascript">

		$(document).ready(function(){
		    $('[data-toggle="tooltip"]').tooltip({
		        placement : 'top'
		    });
		});

		var map = L.map('mapid').setView([30, 0], 2);

		L.tileLayer('https://api.tiles.mapbox.com/v4/mapbox.run-bike-hike/{z}/{x}/{y}.png?access_token=pk.eyJ1Ijoicm9oYW5nb2VsOTYiLCJhIjoiY2phbDloNWtpM253ODJ3bG9mNWdiYzQwMiJ9.jZJvg-axeL9dDxyvGVGfkQ', {
			// attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
			noWrap: true,
			maxZoom: 8,
			minZoom: 2,
		}).addTo(map);

		var countryList = []
		{% for post in site.travels reversed %}
			var countryName = "{{post.country}}".trim().toLowerCase();
			if(countryList.indexOf(countryName) == -1 && countryName.length > 0){
				countryList.push(countryName)
			}
		{% endfor %}

		function getOpacity(feature) {
			var countryName = feature.properties.name.toLowerCase();
			if(countryList.indexOf(countryName) > -1){
				return 0.2;
			} else{
				return 0;
			}
		}

		function getRadius(MarkerSize){
			if (MarkerSize=="small") return 5000;
			if (MarkerSize=="small+") return 10000;
			if (MarkerSize=="med") return 15000;
			else if(MarkerSize=="large") return 30000;
			else return 20000;
		}

		countriesLater = L.geoJson(countriesGeoJSON, { style: function(feature) {
		    return {
		      fillColor: "red",
		      fillOpacity: getOpacity(feature),
		      stroke: true,
		      color: "grey",
		      weight: 0
		    };
		  } 
		}).addTo(map);

		{% for post in site.travels reversed %}
			var coordiList = "{{post.coordi}}".split("+");
			var locationNames = "{{post.location}}".split("+");
			var markersizeList = "{{post.MarkerSize}}".split("+");
			
			if("{{post.coordi}}".length > 0){
				coordiList.forEach(function(coordinateString, i){
				var coordinate = coordinateString.replace(/[{()}]/g, '').trim().split(",").map(Number);
				var locationName = locationNames[i];
				var MarkerSize = markersizeList[i];
				if(locationName === undefined){
					locationName = locationNames[0]
				}
				if(MarkerSize === undefined){
					MarkerSize = markersizeList[0];
				}
				var circle = L.circle(coordinate, {
				    color: 'red',
				    fillColor: '#f03',
				    fillOpacity: 0.5,
				    radius: getRadius(MarkerSize.trim())
					}).bindPopup("<a href='{{site.baseurl}}{{post.url}}' target='_blank' >{{post.title}}</a><br><b>"+locationName+", {{post.country}}</b><br>{{post.date | date: '%B %d, %Y'}}").addTo(map);
				})
			}
		{% endfor %}
	</script>
</body>
</html>