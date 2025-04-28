---
layout: page
title: MemExp with People
description: People whom I shared memories with
---

<!-- 
  People Page - Lists all individuals mentioned in posts with "@" 
  This page dynamically generates a list of people and links to posts where they are mentioned
-->

<style>
    /* People page styling */
    .people-intro {
        text-align: center;
        margin-bottom: 2.5rem;
    }
    
    .people-intro h3 {
        font-family: 'Playfair Display', serif;
        font-size: 2rem;
        color: #1A7B88;
        margin-bottom: 0.5rem;
    }
    
    .people-intro p {
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 1.2rem;
    }
    
    .people-count {
        display: inline-block;
        background-color: #1A7B88;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    
    /* Search filter */
    .people-filter {
        margin: 1rem auto 2rem;
        max-width: 500px;
        position: relative;
    }
    
    .people-filter input {
        width: 100%;
        padding: 0.8rem 1rem 0.8rem 2.5rem;
        border: 1px solid #ddd;
        border-radius: 30px;
        font-size: 1rem;
        font-family: 'Open Sans', sans-serif;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }
    
    .people-filter input:focus {
        outline: none;
        border-color: #1A7B88;
        box-shadow: 0 2px 8px rgba(26, 123, 136, 0.2);
    }
    
    .people-filter::before {
        content: "🔍";
        position: absolute;
        left: 1rem;
        top: 50%;
        transform: translateY(-50%);
        color: #999;
        font-size: 1rem;
    }
    
    .people-container {
        display: flex;
        flex-wrap: wrap;
        gap: 1.5rem;
        margin-top: 1.5rem;
    }
    
    .people-column {
        flex: 1;
        min-width: 45%;
    }
    
    .person-card {
        margin-bottom: 1.5rem;
        padding: 1rem;
        border-radius: 8px;
        transition: all 0.3s ease;
        background-color: #fff;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    .person-card:hover {
        background-color: rgba(26, 123, 136, 0.05);
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    .person-name {
        font-weight: 600;
        font-family: 'Montserrat', sans-serif;
        font-size: 1.3rem;
        margin-bottom: 0.7rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid rgba(26, 123, 136, 0.2);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .person-name a {
        color: #1A7B88;
        text-decoration: none;
    }
    
    .person-count {
        font-size: 0.8rem;
        color: #666;
        background: rgba(26, 123, 136, 0.1);
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
    }
    
    .person-posts {
        font-size: 1.15rem; /* Increased by 15% from 1rem */
        line-height: 1.6;
        margin-left: 0.5rem;
        color: #444;
    }
    
    .person-posts a {
        display: block;
        margin: 0.4rem 0;
        padding: 0.4rem 0.6rem;
        border-radius: 4px;
        transition: background-color 0.2s ease;
        color: #1A7B88;
        text-decoration: none;
        font-size: 1.2rem; /* Increased by 20% from 1rem */
    }
    
    .person-posts a:hover {
        background-color: rgba(255, 125, 69, 0.1);
        color: #FF7D45;
    }
    
    /* Highlight target person when linked directly */
    :target, .highlight-target {
        background-color: rgba(255, 125, 69, 0.15);
        animation: highlight-fade 2s ease-out;
    }
    
    @keyframes highlight-fade {
        from { background-color: rgba(255, 125, 69, 0.3); }
        to { background-color: rgba(255, 125, 69, 0.15); }
    }
    
    /* Stronger highlight for specific targets */
    .highlight-target {
        box-shadow: 0 0 0 3px rgba(255, 125, 69, 0.5);
    }
    
    /* No results message */
    .no-results {
        text-align: center;
        padding: 2rem;
        font-size: 1.1rem;
        color: #666;
        font-style: italic;
        display: none;
    }
    
    /* Responsive adjustments */
    @media (max-width: 767px) {
        .people-container {
            flex-direction: column;
        }
        
        .people-column {
            width: 100%;
        }
        
        .people-intro h3 {
            font-size: 1.8rem;
        }
        
        .people-filter input {
            font-size: 0.9rem;
            padding: 0.7rem 1rem 0.7rem 2.2rem;
        }
    }
</style>

<div class="people-intro">
    <h3>Travel Companions</h3>
    <p>Friends and family who have shared adventures with me</p>
    <div class="people-count">People: <span id="count">loading...</span></div>
</div>

<div class="people-filter">
    <input type="text" id="name-filter" placeholder="Search for a person..." aria-label="Filter people by name">
</div>

<div class="no-results">No people found matching your search</div>

<div class="people-container">
    <div id="even_container" class="people-column"></div>
    <div id="odd_container" class="people-column"></div>
</div>
<!-- Load jQuery for dynamic content generation -->
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>

<!-- Script to generate people list from post mentions -->
<script type="text/javascript">
    // Object to track all people mentions
    var tracker = {};
    
    // Process all travel posts to find @ mentions
    {% for page in site.travels reversed %}
        {% unless page.url contains 'slideshow' %}
            {% assign post_number = forloop.index %}
            var post_number = {{post_number}};

            // Get post content based on format
            {% if page.photos %}
                {% assign posts = page.photos | map: "caption" %}
            {% else %}
                {% assign posts = page.my_arr | split: "|" %}
            {% endif %}

            // Process each caption/paragraph for @ mentions
            {% for post in posts %}
                {% if post == nil %}
                    {% continue %}
                {% endif %}
                var para = {{post | jsonify }};
                var splittedAt = para.split("@");
                if(splittedAt.length > 1){
                    for (let index = 1; index < splittedAt.length; index++) {
                        const name = splittedAt[index].split(" ")[0].replace(/(^\s*,)|(,\s*$)/g, '').trim().replace(/\.+$/, "").trim();
                        if(name.length > 0){
                            tracking_object = {
                                "post_number": post_number,
                                "title": {{ page.title | jsonify }},
                                "link": "{{ site.baseurl }}{{ page.url }}",
                                "para_number": {{forloop.index}}
                            }
                            if(name in tracker){
                                tracker[name].push(tracking_object)
                            } else {
                                tracker[name] = [tracking_object]
                            }
                        }
                    }
                }
            {% endfor %}
            
            // Handle legacy post format
            if("{{page.layout}}" == "post_layout"){
                var oldTypePostText = "{{ page.content | jsonify | smartify | replace: '</', ''}}";
                var splittedAt = oldTypePostText.split("@");
                if(splittedAt.length > 1){
                    for (let index = 1; index < splittedAt.length; index++) {
                        var name = splittedAt[index].split(" ")[0].split("&")[0].replace(/(^\s*,)|(,\s*$)/g, '').trim().replace(/\.+$/, "").trim()
                        if(name.length > 0){
                            tracking_object = {
                                "post_number": post_number,
                                "title": {{ page.title | jsonify }},
                                "link": "{{ site.baseurl }}{{ page.url }}",
                                "para_number": ""
                            }
                            if(name in tracker){
                                tracker[name].push(tracking_object)
                            } else {
                                tracker[name] = [tracking_object]
                            }
                        }
                    }
                }
            }
        {% endunless %}
    {% endfor %}
    
    // When document is ready, generate the people list
    $(document).ready(function() {
        var body_e = $("#even_container");
        var body_o = $("#odd_container");
        var count = 0;
        var allPersonCards = []; // Store all person cards for filtering
        
        // Sort names alphabetically
        names = Object.keys(tracker);
        names.sort();
        
        // Generate HTML for each person
        for(let index = 0; index < names.length; index++){
            var name = names[index];
            var post_numbers = [];
            var post_for_name = 0;
            var postLinks = '';
            
            // First, group mentions by post to find the last paragraph number for each post
            var postMentions = {};
            
            // Group all mentions by post number
            for(var i = 0; i < tracker[name].length; i++) {
                var obj = tracker[name][i];
                var postNum = obj.post_number;
                
                if(!postMentions[postNum]) {
                    postMentions[postNum] = [];
                }
                postMentions[postNum].push(obj);
            }
            
            // Now create links showing all mentions but linking to the last one
            for(var postNum in postMentions) {
                var mentions = postMentions[postNum];
                var lastMention = mentions[mentions.length - 1]; // Get the last mention for the link
                
                var linkText = lastMention.title;
                var linkUrl = lastMention.link;
                var lastParaNum = lastMention.para_number;
                
                // Add paragraph anchor if available
                if (lastParaNum && lastParaNum !== "") {
                    linkUrl += "#" + lastParaNum;
                }
                
                // Collect all paragraph numbers for display
                var allParaNums = [];
                for(var j = 0; j < mentions.length; j++) {
                    if(mentions[j].para_number && mentions[j].para_number !== "") {
                        allParaNums.push(mentions[j].para_number);
                    }
                }
                
                // Add paragraph numbers to link text if available
                if(allParaNums.length > 0) {
                    linkText += " #" + allParaNums.join(", #");
                }
                
                postLinks += "<a href='" + linkUrl + "'>" + linkText + "</a>";
                post_for_name += 1;
            }
            
            // Create person card with name and post links
            var personCard = $('<div class="person-card" id="' + name + '" data-name="' + name.toLowerCase() + '"></div>');
            personCard.append('<div class="person-name"><a href="#' + name + '">' + name + '</a><span class="person-count">' + post_for_name + '</span></div>');
            personCard.append('<div class="person-posts">' + postLinks + '</div>');
            
            // Store the card for filtering
            allPersonCards.push({
                element: personCard,
                name: name.toLowerCase(),
                column: count % 2 === 0 ? 'even' : 'odd'
            });
            
            // Add to appropriate column for balanced layout
            if(count % 2 == 0){
                body_e.append(personCard);
            } else {
                body_o.append(personCard);
            }
            count += 1;
        }
        
        // Update the people count
        $("#count").html(count);
        
        // Filter functionality
        $("#name-filter").on("input", function() {
            var searchTerm = $(this).val().toLowerCase().trim();
            var visibleCount = 0;
            var evenCount = 0;
            var oddCount = 0;
            
            // Clear columns
            body_e.empty();
            body_o.empty();
            
            // Filter and redistribute cards to maintain balance
            for(var i = 0; i < allPersonCards.length; i++) {
                var card = allPersonCards[i];
                
                if(searchTerm === "" || card.name.indexOf(searchTerm) > -1) {
                    // Show cards that match the filter
                    if(evenCount <= oddCount) {
                        body_e.append(card.element);
                        evenCount++;
                    } else {
                        body_o.append(card.element);
                        oddCount++;
                    }
                    visibleCount++;
                }
            }
            
            // Show/hide no results message
            if(visibleCount === 0) {
                $(".no-results").show();
            } else {
                $(".no-results").hide();
            }
            
            // Update count
            $("#count").html(visibleCount);
        });
        
        // Handle hash in URL for direct linking
        function handleHash() {
            if(window.location.hash) {
                var hash = window.location.hash.substring(1);
                var element = document.getElementById(hash);
                
                if(element) {
                    // Scroll to the element
                    setTimeout(function() {
                        element.scrollIntoView({behavior: 'smooth', block: 'center'});
                        
                        // Add highlight class
                        element.classList.add('highlight-target');
                        
                        // Remove highlight after animation completes
                        setTimeout(function() {
                            element.classList.remove('highlight-target');
                        }, 2000);
                    }, 300);
                }
            }
        }
        
        // Handle hash on page load
        handleHash();
        
        // Handle hash changes (e.g., when clicking on person links)
        window.addEventListener('hashchange', handleHash);
    });
</script>
