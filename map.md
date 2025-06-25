---
layout: page
title: MemExp on Map
description: Map showcasing the travelled places.
---

<!-- Map Page - Interactive visualization of travel locations -->

<style type="text/css">
    /* Map page styling */
    .map-intro {
        text-align: center;
        margin-bottom: 1.5rem;
    }
    
    .map-intro h3 {
        font-family: 'Playfair Display', serif;
        font-size: 2rem;
        color: #1A7B88;
        margin-bottom: 0.5rem;
    }
    
    .map-intro p {
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 1rem;
    }
    
    .map-tip {
        background-color: rgba(26, 123, 136, 0.1);
        padding: 0.8rem;
        border-radius: 8px;
        margin: 1rem 0;
        font-size: 1rem;
        color: #333;
        display: inline-block;
    }
    
    .map-tip strong {
        color: #1A7B88;
    }
    
    /* Make the map container take up more horizontal space */
    .eight.columns.main-content-area {
        width: 100%;
        margin-left: 0;
    }
    
    #mapid {
        height: 550px;
        width: 100%;
        border-radius: 12px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.15);
        margin-bottom: 2rem;
        overflow: hidden;
    }
    
    .leaflet-container {
        background-color: #8BD1E3 !important;
        border-radius: 12px;
    }
    
    /* Modern popup styling with less blank space */
    .leaflet-popup-content-wrapper {
        border-radius: 8px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.2);
        padding: 0;
        overflow: hidden;
        min-width: 200px;
    }
    
    .leaflet-popup-content {
        margin: 0;
        font-family: 'Montserrat', sans-serif;
        line-height: 1.2;
    }
    
    .leaflet-popup-content a {
        color: #1A7B88;
        font-weight: 600;
        font-size: 1.3rem;
        display: block;
        margin-bottom: 2px;
        text-decoration: none;
    }
    
    .leaflet-popup-content a:hover {
        color: #FF7D45;
    }
    
    .leaflet-popup-content div {
        margin: 2px 0;
    }
    
    .leaflet-popup-tip {
        background-color: white;
    }
    
    .leaflet-popup-close-button {
        color: #666;
        font-size: 16px;
        padding: 6px;
    }
    
    .map-controls {
        text-align: center;
        margin: 1rem 0;
    }
    
    .map-controls button {
        background: #1A7B88;
        color: white;
        border: none;
        padding: 8px 15px;
        margin: 0 5px;
        border-radius: 4px;
        cursor: pointer;
        font-size: 0.9rem;
        transition: background-color 0.3s;
    }
    
    .map-controls button:hover {
        background: #FF7D45;
    }
    
    /* Flag styling */
    .countries-section {
        margin-top: 2rem;
        text-align: center;
    }
    
    .countries-section h4 {
        font-family: 'Playfair Display', serif;
        font-size: 2rem;
        color: #1A7B88;
        margin-bottom: 1rem;
        position: relative;
    }
    
    .countries-section h4:after {
        content: '';
        display: block;
        width: 60px;
        height: 3px;
        background: #FF7D45;
        margin: 10px auto;
    }
    
    .flag-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 0.5rem;
        max-width: 1000px;
        margin: 0 auto;
    }
    
    .flag-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin: 0.5rem;
        transition: transform 0.3s ease;
    }
    
    .flag-item:hover, .flag-item.highlighted {
        transform: translateY(-5px);
    }
    
    .flag-item.highlighted .flag-icon {
        box-shadow: 0 0 8px #FF7D45;
        border: 1px solid #FF7D45;
    }
    
    .flag-icon {
        font-size: 3em !important;
        border: 1px solid #eee;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        border-radius: 4px;
        margin-bottom: 0.5rem;
    }
    
    .flag-name {
        font-size: 1rem;
        color: #333;
        font-family: 'Montserrat', sans-serif;
        text-align: center;
        max-width: 100px;
        overflow: hidden;
        text-overflow: ellipsis;
        font-weight: 500;
    }
    
    .country-count {
        display: inline-block;
        background-color: #1A7B88;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.9rem;
        margin-top: 1rem;
    }
    
    /* Responsive adjustments */
    @media (max-width: 767px) {
        #mapid {
            height: 450px;
        }
        
        .map-intro h3 {
            font-size: 1.8rem;
        }
        
        .flag-container {
            gap: 0.3rem;
        }
        
        .flag-item {
            margin: 0.3rem;
        }
        
        .flag-icon {
            font-size: 2.5em !important;
        }
        
        .flag-name {
            font-size: 0.9rem;
            max-width: 80px;
        }
    }
    
    @media (max-width: 550px) {
        #mapid {
            height: 400px;
        }
    }
</style>

<!-- Map libraries -->
<link rel="stylesheet" type="text/css" href="css/flags/flag-icon.min.css">
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.3.1/dist/leaflet.css"
integrity="sha512-Rksm5RenBEKSKFjgI3a41vrjkw4EVPlJ3+OiI65vTjIdo9brlAacEuKOiQ5OFh7cOI1bkDwLqdLw3Zg0cRJAAQ=="
crossorigin=""/>
<script src="{{ site.url }}{{site.baseurl}}/js/country.js"></script>
<script src="https://unpkg.com/leaflet@1.3.1/dist/leaflet.js"
integrity="sha512-/Nsx9X4HebavoBvEBuyp3I7od5tA0UzAxs+j83KgC8PU0kgB4XiK4Lfe4y4cgBtaRJQEIFCW+oC506aPT2L1zw=="
crossorigin=""></script>

<!-- Map introduction -->
<div class="map-intro">
    <h3>Travel Map</h3>
    <p>Visual journey through all the places I've visited</p>
    <div class="map-tip">
        <strong>Tip:</strong> Zoom in and click on the circles to see photos from each location. Click on countries or flags to zoom to them.
    </div>
</div>

<!-- Map container -->
<div id="mapid"></div>

<!-- Countries section -->
<div class="countries-section">
    <h4><span id="country-count">0</span> Countries Visited</h4>
    <!-- Flag icons with names -->
    <div class="flag-container" id="flag-container">
        <!-- Flags will be generated by JavaScript -->
    </div>
</div>
<!-- JavaScript libraries -->
<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>

<!-- Map initialization script -->
<script type="text/javascript">
    $(document).ready(function(){
        // Parse URL parameters to highlight specific location
        function getUrlParameter(name) {
            name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
            var regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
            var results = regex.exec(location.search);
            return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
        }
        
        var highlightLocation = getUrlParameter('location');
        var highlightCountry = getUrlParameter('country');
        var highlightCoordi = getUrlParameter('coordi');
        // Country data array - extendible format
        var countries = [
            { code: "in", name: "India" },
            { code: "ie", name: "Ireland" },
            { code: "fr", name: "France" },
            { code: "be", name: "Belgium" },
            { code: "nl", name: "Netherlands" },
            { code: "mc", name: "Monaco" },
            { code: "es", name: "Spain" },
            { code: "th", name: "Thailand" },
            { code: "us", name: "USA" },
            { code: "my", name: "Malaysia" },
            { code: "ae", name: "UAE" },
            { code: "ca", name: "Canada" },
            { code: "mx", name: "Mexico" },
            { code: "tr", name: "Turkey" },
            { code: "sg", name: "Singapore" },
            { code: "qa", name: "Qatar" },
            { code: "va", name: "Vatican" },
            { code: "it", name: "Italy" },
            { code: "sm", name: "San Marino" },
            { code: "pt", name: "Portugal" },
            { code: "kr", name: "South Korea" },
            { code: "et", name: "Ethiopia" },
            { code: "hk", name: "Hong Kong" },
            { code: "de", name: "Germany" },
            { code: "cz", name: "Czech Republic" },
            { code: "sk", name: "Slovakia" },
            { code: "at", name: "Austria" },
            { code: "hr", name: "Croatia" },
            { code: "si", name: "Slovenia" },
            { code: "hu", name: "Hungary" },
            { code: "gr", name: "Greece" }
        ];
        
        // Generate flag items without index
        var flagContainer = $('#flag-container');
        var flagItems = {}; // Store flag items by country name for easy access
        
        countries.forEach(function(country) {
            var flagItem = $('<div class="flag-item" data-country="' + country.name.toLowerCase() + '"></div>');
            flagItem.append('<span class="flag-icon flag-icon-' + country.code + '"></span>');
            flagItem.append('<span class="flag-name">' + country.name + '</span>');
            flagContainer.append(flagItem);
            
            // Store reference to flag item
            flagItems[country.name.toLowerCase()] = flagItem;
            
            // Add hover and click events to flag item
            flagItem.on('mouseenter', function() {
                var countryName = $(this).data('country');
                highlightCountryOnMap(countryName);
            });
            
            flagItem.on('mouseleave', function() {
                resetMapHighlights();
            });
            
            // Add click event to flag item to zoom to country
            flagItem.on('click', function() {
                var countryName = $(this).data('country');
                zoomToCountry(countryName);
            });
        });
        
        // Function to highlight country on map
        function highlightCountryOnMap(countryName) {
            countriesLayer.eachLayer(function(layer) {
                var layerCountryName = layer.feature.properties.name.toLowerCase();
                if (layerCountryName === countryName) {
                    layer.setStyle({
                        fillOpacity: 0.5,
                        weight: 2,
                        color: '#FF7D45'
                    });
                    layer.bringToFront();
                }
            });
        }
        
        // Function to zoom to country
        function zoomToCountry(countryName) {
            // Reset all highlights first
            resetAllHighlights();
            
            countriesLayer.eachLayer(function(layer) {
                var layerCountryName = layer.feature.properties.name.toLowerCase();
                if (layerCountryName === countryName) {
                    // Get country bounds and zoom to it
                    var bounds = layer.getBounds();
                    map.fitBounds(bounds, {
                        padding: [50, 50], // Add some padding
                        maxZoom: 6, // Limit zoom level
                        animate: true
                    });
                    
                    // Highlight the country
                    layer.setStyle({
                        fillOpacity: 0.5,
                        weight: 2,
                        color: '#FF7D45'
                    });
                    
                    // Highlight corresponding flag
                    if (flagItems[countryName]) {
                        flagItems[countryName].addClass('highlighted');
                    }
                }
            });
        }
        
        // Function to reset all highlights (both countries and flags)
        function resetAllHighlights() {
            // Reset country highlights
            countriesLayer.eachLayer(function(layer) {
                layer.setStyle({
                    fillOpacity: getOpacity(layer.feature),
                    weight: 0,
                    color: 'grey'
                });
            });
            
            // Reset flag highlights
            for (var countryName in flagItems) {
                flagItems[countryName].removeClass('highlighted');
            }
        }
        
        // Function to reset map highlights
        function resetMapHighlights() {
            countriesLayer.eachLayer(function(layer) {
                var countryName = layer.feature.properties.name.toLowerCase();
                layer.setStyle({
                    fillOpacity: getOpacity(layer.feature),
                    weight: 0,
                    color: 'grey'
                });
            });
        }
        
        // Update country count in heading
        $('#country-count').text(countries.length);
        
        // Initialize map
        var map = L.map('mapid').setView([30, 0], 2);
        
        // Add click handler to map to reset highlights when clicking on empty space
        map.on('click', function() {
            resetAllHighlights();
        });
        
        // Add custom reset button to map controls
        L.Control.ResetView = L.Control.extend({
            options: {
                position: 'topleft'
            },
            
            onAdd: function(map) {
                var container = L.DomUtil.create('div', 'leaflet-bar leaflet-control leaflet-control-custom');
                container.style.backgroundColor = 'white';
                container.style.width = '30px';
                container.style.height = '30px';
                container.style.cursor = 'pointer';
                container.style.display = 'flex';
                container.style.justifyContent = 'center';
                container.style.alignItems = 'center';
                container.style.fontWeight = 'bold';
                container.style.fontSize = '18px';
                container.style.color = '#666';
                container.innerHTML = '⟲';
                container.title = 'Reset to default view';
                
                container.onclick = function() {
                    // Reset map view to default
                    map.setView([25, 0], 1.8);
                    // Reset all highlights
                    resetAllHighlights();
                }
                
                return container;
            }
        });
        
        // Add the reset button to the map
        new L.Control.ResetView().addTo(map);
        
        // Add map tiles
        var outdoorLayer = L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
            attribution: '',
            maxZoom: 10,
            minZoom: 2,
            id: 'mapbox/outdoors-v11',
            tileSize: 512,
            zoomOffset: -1,
            accessToken: 'pk.eyJ1Ijoicm9oYW5nb2VsOTYiLCJhIjoiY2phbDloNWtpM253ODJ3bG9mNWdiYzQwMiJ9.jZJvg-axeL9dDxyvGVGfkQ'
        }).addTo(map);
        
        // Store all markers for zooming functionality
        var allMarkers = [];
        
        // Build country list from posts
        var countryList = []
        {% for post in site.travels reversed %}
            var countryName = "{{post.country}}".trim().toLowerCase();
            if(countryList.indexOf(countryName) == -1 && countryName.length > 0){
                countryList.push(countryName)
            }
        {% endfor %}
        
        // Set opacity for visited countries
        function getOpacity(feature) {
            var countryName = feature.properties.name.toLowerCase();
            if(countryList.indexOf(countryName) > -1){
                return 0.3; // Increased opacity for better visibility
            } else{
                return 0;
            }
        }
        
        // Get marker radius based on size
        function getRadius(MarkerSize){
            if (MarkerSize=="small") return 5000;
            if (MarkerSize=="smallx") return 10000;
            if (MarkerSize=="med") return 15000;
            if (MarkerSize=="medx") return 22500;
            else if(MarkerSize=="large") return 30000;
            else return 20000;
        }
        
        // Add country polygons with highlighting
        var countriesLayer = L.geoJson(countriesGeoJSON, { 
            style: function(feature) {
                return {
                  fillColor: "#1A7B88", // Updated to match blog color scheme
                  fillOpacity: getOpacity(feature),
                  stroke: true,
                  color: "grey",
                  weight: 0
                };
            },
            onEachFeature: function(feature, layer) {
                // Add hover and click effects
                layer.on({
                    mouseover: function(e) {
                        var countryName = feature.properties.name.toLowerCase();
                        if(countryList.indexOf(countryName) > -1) {
                            layer.setStyle({
                                fillOpacity: 0.5,
                                weight: 2,
                                color: '#FF7D45'
                            });
                            
                            // Highlight corresponding flag
                            if (flagItems[countryName]) {
                                flagItems[countryName].addClass('highlighted');
                                
                                // Scroll to the flag if it's not visible
                                var flagsContainer = document.querySelector('.flag-container');
                                var flagElement = flagItems[countryName][0];
                                var containerRect = flagsContainer.getBoundingClientRect();
                                var flagRect = flagElement.getBoundingClientRect();
                                
                                if (flagRect.bottom > containerRect.bottom || flagRect.top < containerRect.top) {
                                    flagElement.scrollIntoView({behavior: 'smooth', block: 'center'});
                                }
                            }
                        }
                    },
                    mouseout: function(e) {
                        layer.setStyle({
                            fillOpacity: getOpacity(feature),
                            weight: 0,
                            color: 'grey'
                        });
                        
                        // Remove highlight from flag
                        var countryName = feature.properties.name.toLowerCase();
                        if (flagItems[countryName]) {
                            flagItems[countryName].removeClass('highlighted');
                        }
                    },
                    click: function(e) {
                        var countryName = feature.properties.name.toLowerCase();
                        if(countryList.indexOf(countryName) > -1) {
                            // Reset all highlights first
                            resetAllHighlights();
                            
                            // Get country bounds and zoom to it
                            var bounds = layer.getBounds();
                            map.fitBounds(bounds, {
                                padding: [50, 50], // Add some padding
                                maxZoom: 6, // Limit zoom level
                                animate: true
                            });
                            
                            // Highlight the country
                            layer.setStyle({
                                fillOpacity: 0.5,
                                weight: 3,
                                color: '#FF7D45'
                            });
                            
                            // Highlight corresponding flag
                            if (flagItems[countryName]) {
                                flagItems[countryName].addClass('highlighted');
                            }
                            
                            // Prevent the click from propagating to the map
                            L.DomEvent.stopPropagation(e);
                        }
                    }
                });
            },
            // Set z-index to ensure countries are below markers
            pane: 'tilePane'
        }).addTo(map);
        
        // Store circles and their base radii for zoom adjustment
        var circles = [];
        var baseRadii = [];
        
        // Create a separate pane for markers to ensure they're always on top
        map.createPane('markersPane');
        map.getPane('markersPane').style.zIndex = 650; // Higher than the default overlay pane (400)
        
        // Add location markers
        {% for post in site.travels reversed %}
            {% unless post.url contains 'slideshow' %}
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
                        locationName = locationName.trim()
                        if(MarkerSize === undefined){
                            MarkerSize = markersizeList[0];
                        }
                        // Create circle with base radius
                        var baseRadius = getRadius(MarkerSize.trim());
                        var circle = L.circle(coordinate, {
                            color: '#FF7D45',
                            fillColor: '#f03',
                            fillOpacity: 0.5,
                            radius: baseRadius,
                            weight: 2,
                            pane: 'markersPane' // Use the markers pane to ensure they're on top
                        }).bindPopup("<a href='{{site.baseurl}}{{post.url | remove: '/post'}}' target='_blank'>{{post.title}}</a><div><b>"+locationName+", {{post.country}}</b></div><div style='color:#666; font-size:0.85rem;'>{{post.date | date: '%B %d, %Y'}}</div>").addTo(map);
                        
                        // Store circle and its base radius for zoom adjustment
                        circles.push(circle);
                        baseRadii.push(baseRadius);
                        
                        // Add pulse animation on hover
                        circle.on('mouseover', function() {
                            this.setStyle({
                                fillOpacity: 0.8
                            });
                        });
                        
                        circle.on('mouseout', function() {
                            this.setStyle({
                                fillOpacity: 0.5
                            });
                        });
                        
                        // Store marker for zooming functionality
                        allMarkers.push(circle);
                    })
                }
            {% endunless %}
        {% endfor %}
        
        // Set view to show more of the northern hemisphere
        map.setView([25, 0], 1.8);
        
        // If URL parameters are present, find and highlight the marker
        if (highlightLocation && highlightCoordi) {
            // Wait a bit for all markers to be added
            setTimeout(function() {
                var foundMarker = false;
                
                // Try to find the marker based on coordinates
                var coordiList = highlightCoordi.split("+");
                if (coordiList.length > 0) {
                    var targetCoordinate = coordiList[0].replace(/[{()}]/g, '').trim().split(",").map(Number);
                    
                    // Look through all markers
                    for (var i = 0; i < circles.length; i++) {
                        var markerLatLng = circles[i].getLatLng();
                        
                        // Check if coordinates match (with some tolerance)
                        if (Math.abs(markerLatLng.lat - targetCoordinate[0]) < 0.01 && 
                            Math.abs(markerLatLng.lng - targetCoordinate[1]) < 0.01) {
                            
                            // Open the popup and zoom to the marker
                            circles[i].openPopup();
                            map.setView([targetCoordinate[0], targetCoordinate[1]], 5);
                            
                            // Highlight the marker
                            circles[i].setStyle({
                                fillOpacity: 0.9,
                                weight: 4
                            });
                            
                            foundMarker = true;
                            break;
                        }
                    }
                }
                
                // If marker not found by coordinates, try to find by location name
                if (!foundMarker && highlightLocation) {
                    // This is a fallback and may not be as accurate
                    console.log("Could not find marker by coordinates, trying by location name");
                }
            }, 500); // Wait 500ms for all markers to be added
        }
        
        // Adjust all circle radii on zoom
        map.on('zoomend', function() {
            var currentZoom = map.getZoom();
            var zoomFactor = Math.pow(1.5, currentZoom - 2); // Base zoom level is 2, increased factor for more dramatic effect
            
            // Update all circles with new radii
            for (var i = 0; i < circles.length; i++) {
                // Scale between 0.5x and 2.0x of original size based on zoom level
                circles[i].setRadius(baseRadii[i] * Math.max(0.5, Math.min(zoomFactor, 2.0)));
            }
        });
        
        // Reset country styles to default (not highlighted)
        countriesLayer.setStyle(function(feature) {
            var countryName = feature.properties.name.toLowerCase();
            if(countryList.indexOf(countryName) > -1) {
                return {
                    fillColor: "#FF7D45",
                    fillOpacity: 0.3, // Lower opacity by default
                    stroke: true,
                    color: "grey",
                    weight: 0
                };
            } else {
                return {
                    fillOpacity: 0,
                    weight: 0
                };
            }
        });
        
        // Add fade-in animation for page elements
        document.addEventListener('DOMContentLoaded', function() {
            var elements = document.querySelectorAll('.map-intro, #mapid, .countries-section');
            elements.forEach(function(el, index) {
                setTimeout(function() {
                    el.classList.add('fade-in');
                }, index * 100);
            });
        });
    });
</script>
