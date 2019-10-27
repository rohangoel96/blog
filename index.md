---
layout: page
title: MemExp
description: MEMories and EXPeriences. I like to see new things, do stuff, and take pictures.
---

<center>
I like to see new things, do stuff, and take pictures.<br>Photographs, I believe are the best way to preserve our favorite memories and experiences - which otherwise get lost in our over burdened brains.<br>Pretty sure that as a visitor, you think that website deserves to be voted as the most useless thing online - but probably this is for myself and the amazing people I shared these <strong>MemExps</strong> with :) 
<br>
<a href="{{site.baseurl}}/map" style="font-size: 0.8em; position: relative; top: 10px">Checkout the MemExps on the <strong>world map</strong></a>
</center> 

{% assign thisyear = 'now' | date: "%Y" %}
{% assign firstyear = true %}

{% for post in site.travels reversed %}
  {% assign last_post_year = thisyear %}
  {% assign thisyear = post.date | date: "%Y" %}

  {% if firstyear == true or thisyear != last_post_year %}

  {% if thisyear != '2001' %}
  <div class="clear">&nbsp;</div>
  {% endif %}

  <h4 class="years">{{ thisyear }}</h4>
  {% assign firstyear = false %}
{% endif %}

  <div class="blogthumb">
    <a href="{{site.baseurl}}{{post.url}}"><img src="{{site.baseurl}}{{ post.image }}"></a>
    <div class="blogthumb-link"><a href="{{site.baseurl}}{{post.url}}">{{ post.title }}</a></div>
  </div>
    
{% endfor %}

<div class="clear">&nbsp;</div>