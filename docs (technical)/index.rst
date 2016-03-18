.. Schema documentation master file, created by
   sphinx-quickstart on Sat Feb 13 13:27:50 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to the `Schema Generator` documentation!
================================================

Contents:

.. toctree::
    :maxdepth: 2

    model
    view
    controller
    javascript
    apache
    schema_bot

This software is meant to serve as a tool for creating valid |schema.org| |external_link| markups. These can then be used by web developers to improve the SEO of the websites they maintain.

For instance

.. raw:: html

    <div class="highlight-html"><div class="highlight"><pre><span class="nt">&lt;div</span> <span class="na">itemscope</span> <span class="na">itemtype=</span><span class="s">&quot;http://schema.org/Park&quot;</span><span class="nt">&gt;</span>
        <span class="nt">&lt;div</span> <span class="na">itemprop=</span><span class="s">geo</span> <span class="na">itemscope</span> <span class="na">itemtype=</span><span class="s">&quot;http://schema.org/GeoCoordinates&quot;</span><span class="nt">&gt;</span>
            <span class="nt">&lt;span</span> <span class="na">itemprop=</span><span class="s">&quot;latitude&quot;</span><span class="nt">&gt;</span>44.4279668<span class="nt">&lt;/span&gt;</span>
            <span class="nt">&lt;span</span> <span class="na">itemprop=</span><span class="s">&quot;longitude&quot;</span><span class="nt">&gt;</span>-110.5906437<span class="nt">&lt;/span&gt;</span>
        <span class="nt">&lt;/div&gt;</span>
        <span class="nt">&lt;span</span> <span class="na">itemprop=</span><span class="s">&quot;hasMap&quot;</span><span class="nt">&gt;</span>http://www.nps.gov/common/commonspot/customcf/apps/maps/showmap.cfm?alphacode=yell&amp;parkname=Yellowstone<span class="nt">&lt;/span&gt;</span>
        <span class="nt">&lt;span</span> <span class="na">itemprop=</span><span class="s">&quot;name&quot;</span><span class="nt">&gt;</span>Yellowstone<span class="nt">&lt;/span&gt;</span>
        <span class="nt">&lt;span</span> <span class="na">itemprop=</span><span class="s">&quot;url&quot;</span><span class="nt">&gt;</span>http://www.nps.gov/yell/index.htm<span class="nt">&lt;/span&gt;</span>
    <span class="nt">&lt;/div&gt;</span>
    </pre></div>
    </div>

To maintain an up-to-date version of the hierarchy, the |Schema bot| can be set-up with a ``cron`` job

The |Application Server| can be started, concurrently, listening to different ports. The |Web Server| should be configured for load balancing to these different ports.

Programming languages:

* |Python 3.4| |external_link| - All server side code

* |Javascript| |external_link| - AJAX functionality and persistence

Copyright information
=====================

Refer to the |Readme.txt| file for © copyright information


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. |Readme.txt| raw:: html

   <a href="Readme.txt">Readme.txt</a>

.. |Python 3.4| raw:: html

   <a href="https://docs.python.org/3.4/" target="_blank">Python 3.4</a>

.. |Javascript| raw:: html

   <a href="https://en.wikipedia.org/wiki/JavaScript" target="_blank">Javascript</a>
