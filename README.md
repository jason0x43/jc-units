[Alfred 2][alfred] Workflow for unit conversion
===============================================

<p align="center">
<img alt="Screenshot" src="http://dl.dropbox.com/s/gmep3v3hc5tvn57/jc-units_screenshot.png" />
</p>

<p align="center">
  <a href="http://dl.dropbox.com/s/kxzv83fkpw7caow/jc-units.alfredworkflow"><img src="http://dl.dropbox.com/s/m823ene4il9cnac/dl_button.png" alt="Download"></a>
</p>

This is a really simple workflow that uses the <a href="https://github.com/hgrecco/pint">Pint</a>
unit library to convert an input string. The calculator is called as you type,
so as soon as you put in something it considers valid, you'll see output.

Actioning the result will copy the value (just the number) to the clipboard.
That's it!

Basic conversion is performed with a command like:

    u {value} {in units} > {out units}

You can include a space after the `u` keyword, but it's not required. Units can
generally be abbreviated or not, as long as the input is unambiguous. A greater
than sign (>) is required between the input value and output units. Some example
commands:

* `u 5k > miles`
* `u5k>miles`
* `u5k>mi`

You can also do more advanced queries that use unit math, like:

    u 1cm + 1in - 1mm > in

or

    u 1cm * 1mm > in^2

Installation
------------

To install, just download the [prepackaged workflow][pkg].  Double-click on the
downloaded file, or drag it into the Alfred Workflows window, and Alfred should
install it.


Configuration
-------------

Three options can be set in the workflow configuration file (accessible via the 'u>' command):

* separator - separator to use between input value and output units; default is **">"**
* precision - if set to an integer value, this is the number of digits to include after a decimal point; default is **null**
* loglevel - what level of messages to send to the debug log; default is **"INFO"**


Requirements
------------

* Python 2.7 (standard in Lion and Mountain Lion)
* My [jcalfred][jcalfred] python library (included in the workflow download)

Credits
-------

Currency exchange rates are courtesy of Yahoo! Finance.

[pkg]: http://dl.dropbox.com/s/kxzv83fkpw7caow/jc-units.alfredworkflow
[jcalfred]: https://github.com/jason0x43/jcalfred
[alfred]: http://www.alfredapp.com
[icons]: http://www.weathericonsets.com
[wund]: http://www.weatherunderground.com
[fio]: http://forecast.io
