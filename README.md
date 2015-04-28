# Exuberant CTAGS configuration for JavaScript and CoffeeScript

[Exuberant CTAGS](http://ctags.sourceforge.net) doesn't support CoffeeScript
natively and its JavaScript support doesn't handle modern usage.

There are a bunch of sample regex's around to solve this. However I found
they worked most of the time and would fail for some situations. Different sets of 
configurations would fail for different bits of code. How can we unify them?

I wrote some automated tests to check all the different scenarios as any
agile programmer would.  Now we can adjust the configuration and see that
all our situations are handled.

This configuration started from here:
  https://github.com/majutsushi/tagbar/wiki#exuberant-ctags-vanilla
  https://github.com/majutsushi/tagbar/wiki#coffeescript

Incedentally, if you are interested in electronics, check out [Electropoclypse](http://electropocalypse.com)
