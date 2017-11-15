---
layout: page
---

<center>I like to see new things, do stuff, and take pictures.<br>Photographs, I believe are the best way to preserve our favorite memories and experiences - which otherwise get lost in our over burdened brains.<br>Pretty sure that as a visitor, you think that website deserves to be voted as the most useless thing online - but this probably is for myself - to relive my <strong>MemExp</strong>s :)</center> 

{% assign thisyear = 'now' | date: "%B %Y" %}
{% assign firstyear = true %}

{% for post in site.travels reversed %}
  {% assign last_post_year = thisyear %}
  {% assign thisyear = post.date | date: "%B %Y" %}

  {% if firstyear == true or thisyear != last_post_year %}

  {% if thisyear != '2001' %}
  <div class="clear">&nbsp;</div>
  {% endif %}

  <h4>{{ thisyear }}</h4>
  {% assign firstyear = false %}
  <div class="clear">&nbsp;</div>
{% endif %}

  <div class="blogthumb">
    <a href="{{post.url}}"><img src="{{site.baseurl}}{{ post.image }}"></a>
    <div class="blogthumb-link"><a href="{{site.baseurl}}{{post.url}}">{{ post.title }}</a></div>
  </div>
    
{% endfor %}

<div class="clear">&nbsp;</div>
