# Exuberant CTAGS configuration for JavaScript and CoffeeScript

[Exuberant CTAGS](http://ctags.sourceforge.net) doesn't support CoffeeScript
natively and its JavaScript support doesn't handle modern usage.

There are a bunch of sample regex's around to solve this. However I found
they worked most of the time and would fail for some situations. Different sets of 
configurations would fail for different bits of code. How can we unify them?

I wrote some automated tests to check all the different scenarios as any
agile programmer would.  Now we can adjust the configuration and see that
all our situations are handled.

The regex rules in ctags.conf will support these idioms:

## JavaScript
Functions & Methods in various forms:
```
function global_function(a, b){}                -> global_function

var object_class = {                            -> object_class
  constructor: function(){}
  object_method: function(){}                   -> object_method
}

var assigned_function = function(){}            -> asigned_function

Namespace.namespaced_func = function() {}       -> namespaced_function
```

Variables, arrays, objects:
```
var myarray = [1, 2];                           -> myarray
var myobject = {a: 1};                          -> myobject
var myvar = 1;                                  -> myvar
```

jQuery `bind` event handlers
```
$("#foo").bind("dollar_bind_event", function() {        -> "#foo".dollar_bind_event
jQuery('#foo').bind("jquery_bind_event", function() {   -> '#foo'.jquery_bind_event
$(bar).bind("var_bind_event", function() {              -> bar.var_bind_event
```

Symbols in RSpect style tests. 
`describe()` blocks use the first parameter as the symbol name.
`context()` and `it()` blocks include the lines indentation for use in TagBar
so you can sort of see the file's nested structure
```
describe("Dog", function() {                            -> Dog
  describe("bark", function() {                         -> bark
    context("while running", function() {               -> .    while running
      it("is loud", function() {                        -> .      is loud
```

## Coffeescript
Classes and function are identified. When there is a namespace
prefix, or an `@` instance prefix, the symbol name is correctly extracted.
```
create:  ->                                             -> create
@_setWorkspaceXml: (workspace, codeXml) ->              -> _setWorkspaceXml
class stratego.CamperAppEditor extends phaser.State     -> CamperAppEditor
local_function = (gfx, focusObj) ->                     -> local_function
window.global_function = (gfx, focusObj) ->             -> global_function
window.pkg.pkg_function = (gfx, focusObj) ->            -> pkg_function
```

This configuration started from here:

 - https://github.com/majutsushi/tagbar/wiki#exuberant-ctags-vanilla
 - https://github.com/majutsushi/tagbar/wiki#coffeescript

Incedentally, if you are interested in electronics, check out [Electropoclypse](http://electropocalypse.com)
