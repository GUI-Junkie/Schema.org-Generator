Why would you use this software?
================================

"|Schema.org| |external_link| *is a collaborative, community activity with a mission to create, maintain, and promote schema's for structured data on the Internet*" This '*structured data*' helps Search Engines to obtain meaningful information from your website, even if this is ``hidden`` from the user of the website. This can improve the SEO of the websites you maintain.

Depending on your needs, you could use other, existing, tools for adding |Schema.org| |external_link| schemas to your website. *This tool* aims to provide valid |HTML| |external_link| markup that can be used to integrate these schema's into your website.

Example output
==============

Let's look at a quick example. The first HTML block is generated with this tool, the following two blocks are possible transformations.

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

can be changed into

.. code-block:: html

    <body itemscope itemtype="http://schema.org/Park">
        <h1 itemprop="name">Yellowstone</h1>
        <div class="geo" itemprop=geo itemscope itemtype="http://schema.org/GeoCoordinates">
            Latitude: <span itemprop="latitude">44.4279668</span><br/>
            Longitude: <span itemprop="longitude">-110.5906437</span><br/>
        </div>
        <div class="map">
            <iframe itemprop="hasMap" src="http://www.nps.gov/common/commonspot/customcf/apps/maps/showmap.cfm?alphacode=yell&parkname=Yellowstone"></iframe>
        </div>
        <a itemprop="url" href="http://www.nps.gov/yell/index.htm">Go to site</a>
    </body>

The ``hidden`` keyword can be used to hide some information from the markup, while still allowing Search Engines to find this information.

.. code-block:: html

    <body itemscope itemtype="http://schema.org/Park">
        <h1 itemprop="name">Yellowstone</h1>
        <div hidden itemprop=geo itemscope itemtype="http://schema.org/GeoCoordinates">
            Latitude: <span itemprop="latitude">44.4279668</span><br/>
            Longitude: <span itemprop="longitude">-110.5906437</span><br/>
        </div>
        <div class="map">
            <iframe itemprop="hasMap" src="http://www.nps.gov/common/commonspot/customcf/apps/maps/showmap.cfm?alphacode=yell&parkname=Yellowstone"></iframe>
        </div>
        <a itemprop="url" href="http://www.nps.gov/yell/index.htm">Go to site</a>
    </body>

All three HTML blocks can be validated with the |Structured Data Testing Tool| |external_link|.

Multiple schemas can be used simultaneously on one page. For instance, a |LocalBusiness| |external_link| can sell different products (|OfferCatalog| |external_link|).

.. |LocalBusiness| raw:: html

    <a href="http://schema.org/LocalBusiness" target="_blank">LocalBusiness</a>

.. |OfferCatalog| raw:: html

    <a href="http://schema.org/OfferCatalog" target="_blank">OfferCatalog</a>
