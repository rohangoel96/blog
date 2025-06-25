---
layout: page
title: MemExp
description: I have built this blog as a world of photos and videos which act as a gateway for me to retrieve and explore the memories and experiences. Often reflecting upon the past, I think what eventful happened at a specific time - like graduating in August 2018, visiting my first International destination in May 2017 - this for me is worth remembering and I love to explore all these memories again and again!
---

<!-- Introduction Section -->
<div class="home-intro">
  <p>
    I have a weird fear of forgetting life. Often reflecting upon the past, I think what eventful happened at a specific time: like graduating in August 2018, visiting my first International destination in May 2017 - this for me is worth remembering and I love to explore all these memories again and again!
  </p>
  <p>
    However, remembering events is difficult because our brains are not wired for it! The vast majority of our experiences are lost over time, which for me is regretful. Thus, I have built this blog as a world of photos and videos which act as a gateway for me to retrieve and relive the <strong>MemExps</strong>!
  </p>
  <!-- <a href="{{ site.url }}{{site.baseurl}}/map" class="map-link">Checkout the MemExps on the <strong>world map</strong> <i class="fas fa-map-marked-alt"></i></a> -->
</div>

<!-- Travel Posts by Year -->
<div class="posts-container">
  {% assign thisyear = 'now' | date: "%Y" %}
  {% assign firstyear = true %}

  {% for post in site.travels reversed %}
    {% assign last_post_year = thisyear %}
    {% assign thisyear = post.date | date: "%Y" %}

    {% if firstyear == true or thisyear != last_post_year %}
      {% if thisyear != '2001' %}
      <div class="clear"></div>
      {% endif %}

      <h4 class="years">{{ thisyear }}</h4>
      {% assign firstyear = false %}
    {% endif %}

    {% unless post.url contains 'slideshow' %}
    <!-- Post thumbnail with consistent styling -->
    <div class="blogthumb fade-in">
      <a href="{{ site.url }}{{site.baseurl}}{{post.url}}" class="thumb-link">
        <img src="{{ site.url }}{{site.baseurl}}{{ post.image }}" alt="{{ post.title }} in {{ post.location }}, {{ post.country }}" loading="lazy">
      </a>
      <div class="blogthumb-link">
        <a href="{{ site.url }}{{site.baseurl}}{{post.url}}">{{ post.title }}</a>
      </div>
    </div>
    {% endunless %}
  {% endfor %}

  <div class="clear"></div>
</div>
