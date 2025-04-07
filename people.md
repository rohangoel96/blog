---
layout: page
title: MemExp with People
description: People whom I shared memories with
---

<html>
<head>
    <style>
        .name{
            margin-bottom: 0;
            margin-top: 1.5em;
        }
        .post{
            margin-top: -25px;
        }
        #container{
            width: 100%;
        }
        #even_container{
            width: 48%;
            float: left;
            text-overflow: ellipsis;
            overflow: hidden;
        }
         #odd_container{
            width: 48%;
            float: right;
            text-overflow: ellipsis;
            overflow: hidden;
        }
        .name{
            font-weight:700;
            text-overflow: ellipsis;
            overflow: hidden;
            /* font-size: 15px !important; */
        }
        .post{
            font-size: 15px !important;
        }
        :target {
            background-color: #faa;
        }
        @media (max-width:600px) {
            .dontLoadMobile {
                background-image: none !important;
                display: none;
            }
        }
        .namelink{
            color: black !important;
        }
    </style>
</head>
<body>
    <center>
		<span style="font-size: 1em;">List of different people featuring on MemExp</span><br>
        <span style="font-size: 0.8em;">Count = <span id="count">x</span></span>
	</center>
    <hr>
    <div id="container2">
        <div id="even_container"></div>
        <div id="odd_container"></div>
    </div>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
    <script type="text/javascript">
        tracker = {}
		{% for page in site.travels reversed %}
            {% unless page.url contains 'slideshow' %}
                {% assign post_number = forloop.index %}
                var post_number = {{post_number}};

                {% if page.photos %}
                    {% assign posts = page.photos | map: "caption" %}
                {% else %}
                    {% assign posts = page.my_arr | split: "|" %}
                {% endif %}

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
        var body_e = $("#even_container");
        var body_o = $("#odd_container");
        var count = 0;
        names = Object.keys(tracker);
        names.sort();
        for(let index = 0; index < names.length; index++){
            var name = names[index];
            var holder = $('<div class="holder" id="holder_'+name+'"></div>')
            var post = $('<div class="post" id="post_'+name+'"></div>')
            var post_numbers = [];
            var post_for_name = 0;
            for(obj in tracker[name]){
                var current_obj = tracker[name][obj];
                var current_post_number = current_obj.post_number;
                var prepend = "";
                if (current_obj.para_number > 0) prepend = "#";
                if(post_numbers.includes(current_post_number)) {
                    //repeated mention on same page
                    post.append("<a href='"+current_obj.link+"#"+current_obj.para_number+"'> "+prepend+current_obj.para_number+"</a>")
                } else {
                    post_numbers.push(current_post_number);
                    post.append("<br><a href='"+current_obj.link+"#"+current_obj.para_number+"'>"+current_obj.title+prepend+current_obj.para_number+"</a>")
                    post_for_name += 1;
                }
            }
            holder.append("<p class='name' id='"+name+"'><a href='#"+name+"' class='namelink'>"+name+"</a><span class='dontLoadMobile'> ["+post_for_name+"]</span></p>")
            holder.append(post)
            if(count % 2 == 0){
                body_e.append(holder)
            } else {
                body_o.append(holder)
            }
            count += 1;
        }
        $("#count").html(count);
    </script>
</body>
</html>