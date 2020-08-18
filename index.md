---
layout: page
title: MemExp
description: I have built this blog as a world of photos and videos which act as a gateway for me to retrieve and explore the memories and experiences. Often reflecting upon the past, I think what eventful happened at a specific time - like graduating in August 2018, visiting my first International destination in May 2017 - this for me is worth remembering and I love to explore all these memories again and again!
---

<center>
I have a weird fear of forgetting life. Often reflecting upon the past, I think what eventful happened at a specific time: like graduating in August 2018, visiting my first International destination in May 2017 - this for me is worth remembering and I love to explore all these memories again and again!<br>
However, remembering events is difficult because our brains are not wired for it! The vast majority of our experiences are lost over time, which for me is regretful. Thus, I have built this blog as a world of photos and videos which act as a gateway for me to retrieve and explore the <strong>MemExps</strong>!
<br>
<!-- <a href="{{site.baseurl}}/map" style="font-size: 0.8em; position: relative; top: 10px">Checkout the MemExps on the <strong>world map</strong></a> -->
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