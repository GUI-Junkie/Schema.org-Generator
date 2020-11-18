<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
        <meta name="description" content="Schema Generator"/>
        <meta name="robots" content="index, follow"/>
        <link type="image/png" rel="icon" href="/favicon.ico"/>
        <title>{title}</title>
        <link rel="stylesheet" type="text/css" href="/gen_style.css" />
        <script type="text/javascript" src="/schema.js"></script>
    </head>
    <body onload="javascript:onLoad('{buttons}');">
        <div class="header">
            <a class="logo_link" href="/">
                <img src="/logo_gen.jpg" alt="schema.org &lt;Generator&gt;" title="schema.org &lt;Generator&gt;" class="logo"/>
            </a>
            <div class="wrap_release">
                <span class="release">schema.org release: {version}</span>
            </div>
            <div id="saved" style="display:none"><p>The Schema has been saved in Local Storage</p></div>
        </div> <!-- Fin div header !-->
        <div class="wrapper">
            <nav>
                <ul>
                    <li>
                        <a href="/">Home</a>
                    </li>
                    <li>
                        <a href="http://polak.es/gen_help/index.html" target="_blank">Online help <img src="/external_link.png" alt="external link" title="external link" /></a>
                    </li>
                    <li id="SaveButton" style="display:none">
                        <a href="javascript:SaveSchema(true);">Save Schema</a>
                    </li>
                    <li id="GenerateButton" style="display:none">
                        <span>Generate</span>
                        <a href="javascript:GenerateSchema('Microdata');">&nbsp;&nbsp;&nbsp;&nbsp;Microdata</a>
                        <a href="javascript:GenerateSchema('RDFa');">&nbsp;&nbsp;&nbsp;&nbsp;RDFa</a>
                        <a href="javascript:GenerateSchema('JSON');">&nbsp;&nbsp;&nbsp;&nbsp;JSON-LD</a>
                    </li>
                    <li id="RecoveryButton" style="display:none">
                        <a href="javascript:RecoverData();">Recover Data</a>
                    </li>
                    <li id="ClearButton" style="display:none">
                        <a href="javascript:ClearData();">Clear Data</a>
                    </li>
                    <li>
                        <a href="http://schema.org/" target="_blank">Schema.org <img src="/external_link.png" alt="external link" title="external link" /></a>
                    </li>
                    <li>
                        <a href="http://polak.es/en/generator.html" target="_blank">About <img src="/external_link.png" alt="external link" title="external link" /></a>
                    </li>
                </ul>
            </nav>
            <div class="right_col" id="right_col" tabindex="0">
                <form method="POST" action="/GenerateSchema">
                    {form}
                </form>
                <br />
                {output}
            </div>
        <noscript>Your browser does not support JavaScript!</noscript>
        </div>
        <div itemtype="http://schema.org/PostalAddress" itemscope="" itemprop="address" class="footer">
            <span itemprop="name" class="footer_item">Hans Polak</span>
            <span class="footer_item"><a href="tel:+34669765160">+34 669.765.160</a></span>
            <span itemprop="streetAddress" class="footer_item">c/ San Antonio 52</span>
            <span itemprop="postalCode" class="footer_item">10.470</span>
            <span itemprop="addressLocality" class="footer_item">Villanueva de la Vera</span>
            <span class="footer_item">Cáceres, Spain</span>
            <span class="footer_item"><a href="mailto:info@polak.es?subject=Generator">Contact me</a></span>
            <span itemprop="addressRegion" hidden="">CC</span>
            <span itemprop="addressCountry" hidden="">ES</span>
        </div>
        <span itemprop="currenciesAccepted" hidden="">EUR</span>
        <span itemprop="email" hidden="">info@polak.es</span>
        <span itemprop="foundingDate" hidden="">2015-01-01</span>
        <span itemprop="name" hidden="">Hans Polak</span>
        <span itemprop="paymentAccepted" hidden="">Paypal, Electronic Funds Transfer</span>
        <span itemprop="taxID" hidden="">X2.125.374J</span>
        <span itemprop="telephone" hidden="">+34 669.765.160</span>
        <span itemprop="url" hidden="">http://polak.es</span>
        <span itemprop="vatID" hidden="">ES.X21.253.74J</span>
        <div class="under_footer">
            <form target="_top" method="post" action="https://www.paypal.com/cgi-bin/webscr">
                <input value="_s-xclick" name="cmd" type="hidden"/>
                <input value="RXHPLLAMU2XYC" name="hosted_button_id" type="hidden"/>
                <input name="submit" type="image" src="https://www.paypalobjects.com/en_US/ES/i/btn/btn_donateCC_LG.gif" alt="PayPal - The safer, easier way to pay online!" border="0"/>
                <img border="0" height="1" src="https://www.paypalobjects.com/en_US/i/scr/pixel.gif" alt="" width="1"/>
            </form>
        </div>
        <div class="under_footer">© Copyright 2016 - 2020, Hans Polak.<br/>&nbsp;</div>
        <script>
            document.getElementById("right_col").focus();
        </script>
    </body>
</html>
