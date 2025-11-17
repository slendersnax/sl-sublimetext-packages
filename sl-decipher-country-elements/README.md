# decipher-country-rows

a package to help with multi-country projects in Decipher, meant to be used in conjunction with [decipher-sublimetext-clips](https://github.com/slendersnax/decipher-sublimetext-clips)

## installation

see [main page](https://github.com/slendersnax/sl-sublimetext-packages)

## what does it do?

```xml
<row label="r1">Example row</row>
<row label="r2" value="2">Example row</row>
```
- First Country prefix: 1 =>

```xml
<row label="r101">Example row</row>
<row label="r102" value="102">Example row</row>
```

## why?

### the problem

Suppose you have the following setup in Decipher:

```xml
<radio
  label="dCountry"
  where="execute,survey,report"
  optional="1">
  <title>Hidden dummy - Country recode</title>
  <exec>
...
  </exec>
  <row label="r1">Country 1</row>
  <row label="r2">Country 2</row>
  <row label="r3">Country 3</row>
</radio>
<suspend/>

<radio
  label="QRegion">
  <title>Where do you live?</title>
  
  <row label="r1" cond="dCountry.r1">Country 1 Region 1</row>
  <row label="r2" cond="dCountry.r1">Country 1 Region 2</row>
  <row label="r3" cond="dCountry.r2">Country 2 Region 1</row>
  <row label="r4" cond="dCountry.r2">Country 2 Region 2</row>
  <row label="r5" cond="dCountry.r3">Country 3 Region 1</row>
  <row label="r6" cond="dCountry.r3">Country 3 Region 2</row>
</radio>
<suspend/>
```

While this works, it's not very intuitive and gets very cumbersome very quickly when you have a lot of items in each category - in this case regions in each country.

### the solution

We need an attribute in each row that:
- could be used to filter these items
- could 100% be found in data exports

...and we do - two in fact: `label` and `value`. The solution that this package proposes is the following:

```xml
<radio
  label="QRegion"
  rowCond="row.label[:-2] == dCountry.selected.label">
  <title>Where do you live?</title>
  
  <row label="r101" value="101">Country 1 Region 1</row>
  <row label="r102" value="102">Country 1 Region 2</row>
  <row label="r201" value="201">Country 2 Region 1</row>
  <row label="r202" value="202">Country 2 Region 2</row>
  <row label="r301" value="301">Country 3 Region 1</row>
  <row label="r302" value="302">Country 3 Region 2</row>
  <row label="r303" value="303">Country 3 Region 3</row>
  <row label="r304" value="304">Country 3 Region 4</row>
  <row label="r305" value="305">Country 3 Region 5</row>
  <row label="r306" value="306">Country 3 Region 6</row>
  <row label="r307" value="307">Country 3 Region 7</row>
  <row label="r308" value="308">Country 3 Region 8</row>
  <row label="r309" value="309">Country 3 Region 9</row>
  <row label="r310" value="310">Country 3 Region 10</row>
</radio>
<suspend/>
```

## usage

1. select the rows that you want to transform
2. right click and look for `Transform into country elements` or use the Command Palette and search for the same thing
3. enter the prefix that you want to use
4. press enter :)

notes:
- you can make multiple selections of rows, in which case each subsequent selection of rows will increase the prefix that you entered initially
    - e.g. if you entered 1 and have four different selections then they will go `r10x..., r20x..., r30x..., r40x...`
- the `value` attribute **must** be present in order to be transformed

## extra - alternate solutions

You could:
- create separate region questions for each country and show these questions based on the `dCountry` selection

```xml
<radio
  label="QCountry1Region"
  cond="dCountry.r1">
  <title>Where do you live?</title>
  
  <row label="r1">Country 1 Region 1</row>
  <row label="r2">Country 1 Region 2</row>
</radio>
<suspend/>
```

- use [Style Variables](https://forstasurveys.zendesk.com/hc/en-us/articles/4409477116187-Using-Style-Variables-in-the-Survey-XML) instead of modifying the `label` and `value` attributes


```xml
<stylevar name="cs:country" type="string"/>

<radio
  label="QRegion"
  rowCond="row.styles.cs.country == dCountry.selected.label[1:]">
  <title>Where do you live?</title>
  
  <row label="r1" cs:country="1">Country 1 Region 1</row>
  <row label="r2" cs:country="1">Country 1 Region 2</row>
  <row label="r3" cs:country="2">Country 2 Region 1</row>
  <row label="r4" cs:country="2">Country 2 Region 2</row>
  <row label="r5" cs:country="3">Country 3 Region 1</row>
  <row label="r6" cs:country="3">Country 3 Region 2</row>
</radio>
<suspend/>
```